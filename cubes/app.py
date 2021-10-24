import asyncio
import logging
import signal
from typing import Awaitable, Callable

from cubes import abc, buffer, connection, types

log = logging.getLogger(__name__)


async def _default_unhandled_packet_handler(packet_id: int, packet: buffer.ReadBuffer):
    log.debug(
        "Handler for packet id %i and state %s not implemented.",
        packet_id,
        packet.connection.status.name,
    )


class GracefulExit(SystemExit):
    """Exception raising when server should stop."""


class Application(abc.Application):
    """Class for creating Minecraft Java Edition server implemetation."""

    # pylint: disable=W0201

    _handlers: dict[tuple[types.ConnectionStatus, int], Awaitable]

    def __init__(self, packet_read_timeout: int = 20):
        super().__init__(packet_read_timeout)
        self._handlers = {}
        self.unhandled_packet_handler = _default_unhandled_packet_handler

    def run(self, host: str, port: int = 25565) -> None:
        """Starts application."""
        loop = asyncio.get_event_loop()
        try:
            loop.add_signal_handler(signal.SIGINT, self._raise_graceful_exit)
            loop.add_signal_handler(signal.SIGTERM, self._raise_graceful_exit)
        except NotImplementedError:  # signals not implemented on windows
            pass
        log.info("Starting server on %s:%i", host, port)
        try:
            loop.run_until_complete(self._run(host, port))
        finally:
            log.info("Server stopped")

    def add_low_level_handler(
        self, conn_status: types.ConnectionStatus, packet_id: int, func: Callable
    ) -> None:
        """Adds packet handler.

        Raises:
            ValueError: when handler with the same filter (conn_status and packet_id)
                already added

        Examples:
            >>> app.add_low_level_handler(cubes.ConnectionStatus.HANDSHAKE,
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

    async def _run(self, host: str, port: int) -> None:
        try:
            server = await asyncio.start_server(self._accept_connection, host, port)
            await server.serve_forever()
        except Exception as exc:
            log.exception(exc)
            raise GracefulExit from exc

    async def _accept_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        # pylint: disable=W0703
        conn = connection.Connection(reader, writer, self)
        try:
            while True:
                packet = await asyncio.wait_for(
                    self._wait_packet(conn), self._packet_read_timeout
                )
                asyncio.create_task(self._process_packet(conn, packet))
        except asyncio.TimeoutError:
            log.debug("Connection (%s, %i) timed out.", *conn.peername)
        except Exception as exc:
            log.exception(exc)
        finally:
            if not conn.is_closing:
                await conn.close()

    @staticmethod
    async def _wait_packet(conn: connection.Connection) -> abc.AbstractReadBuffer:
        packet = await conn.read_packet()
        while not packet:
            await asyncio.sleep(0.001)
            packet = await conn.read_packet()
        return packet

    async def _process_packet(
        self, conn: connection.Connection, packet: abc.AbstractReadBuffer
    ) -> None:
        # pylint: disable=W0703
        packet_id = packet.varint
        handler = self._handlers.get((conn.status, packet_id))
        handler = handler if handler else self._unhandled_packet_handler
        try:
            await handler(packet_id, packet)
        except connection.CloseConnection as exc:
            await conn.close(exc.reason)
            log.debug(
                "Connection (%s, %i) closed by handler (%s, %i). Reason: %s.",
                *conn.peername,
                conn.status.name,
                packet_id,
                str(exc.reason),
            )
        except Exception as exc:
            log.exception(exc)
