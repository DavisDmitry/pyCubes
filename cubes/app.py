import asyncio
import logging
import signal
from typing import Awaitable, Callable, Optional

from cubes import buffer, connection

# If the client does not send a kee-alive packet within 20 seconds,
# the connection should be closed].
# https://wiki.vg/Protocol#Keep_Alive_.28serverbound.29
_NO_PACKET_TIMEOUT = 20

log = logging.getLogger(__name__)


class GracefulExit(SystemExit):
    """Exception raising when server should stop."""


async def _default_unhandled_packet_handler(packet: buffer.ReadBuffer) -> None:
    packet = buffer.ReadBuffer(packet.data)
    conn = connection.Connection.get_current()
    log.debug(
        "Handler for packet id %i with state %s not implemented.",
        packet.varint,
        conn.status.name,
    )


class Application:
    """Class for creating Minecraft Java Edition server implemetation.

    Examples:
        >>> app = Application('0.0.0.0', 25565)
    """

    _handlers: dict[tuple[connection.ConnectionStatus, int], Awaitable]
    _unhandled_packet_handler: Awaitable

    def __init__(self, host: str, port: int):
        self._host, self._port = host, port
        self._handlers = {}
        self._unhandled_packet_handler = _default_unhandled_packet_handler

    def run(self) -> None:
        """Starts application."""
        loop = asyncio.get_event_loop()
        try:
            loop.add_signal_handler(signal.SIGINT, self._raise_graceful_exit)
            loop.add_signal_handler(signal.SIGTERM, self._raise_graceful_exit)
        except NotImplementedError:  # signals not implemented on windows
            pass
        log.info("Starting server on %s:%i", self._host, self._port)
        try:
            loop.run_until_complete(self._run())
        finally:
            log.info("Server stopped")

    def add_low_level_handler(
        self, conn_status: connection.ConnectionStatus, packet_id: int, func: Callable
    ) -> None:
        """Adds packet handler.

        Raises:
            ValueError: when handler with the same filter (conn_status and packet_id)
                already added

        Examples:
            >>> server.add_low_level_handler(ConnectionStatus.HANDSHAKE,
                    0x00, process_handshake)
        """
        if self._handlers.get((conn_status, packet_id)):
            raise ValueError(
                f"Handler for status {conn_status} and packet "
                f"{packet_id} are already exists."
            )
        self._handlers[(conn_status, packet_id)] = func

    def _change_unhandled_packet_handler(self, func: Callable) -> None:
        self._unhandled_packet_handler = func

    unhandled_packet_handler = property(fset=_change_unhandled_packet_handler)

    @staticmethod
    def _raise_graceful_exit() -> None:
        raise GracefulExit

    async def _run(self) -> None:
        try:
            server = await asyncio.start_server(
                self._accept_connection, self._host, self._port
            )
            await server.serve_forever()
        except Exception as exc:
            log.exception(exc)
            raise GracefulExit from exc

    async def _accept_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        conn = connection.Connection(reader, writer)
        conn.set_current()
        try:
            while True:
                packet = await asyncio.wait_for(
                    self._read_packets(conn), _NO_PACKET_TIMEOUT
                )
                await self._process_packet(conn, packet)
        except connection.CloseConnection:
            log.debug("Connection closed by packet handler.")
        except asyncio.TimeoutError:
            log.debug("Dead connection. Closing.")
        finally:
            await conn.close()

    async def _read_packets(self, conn: connection.Connection) -> buffer.ReadBuffer:
        packet = await conn.read_packet()
        while not packet:
            await asyncio.sleep(0.001)
            packet = await conn.read_packet()
        return packet

    async def _process_packet(
        self, conn: connection.Connection, packet: buffer.ReadBuffer
    ) -> None:
        packet_id = packet.varint
        handler = self._handlers.get((conn.status, packet_id))
        handler = handler if handler else self._unhandled_packet_handler
        _buffer: Optional[buffer.WriteBuffer] = await handler(packet)
        if _buffer:
            await conn.send_packet(_buffer)
