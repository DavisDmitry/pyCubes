import asyncio
import logging
import signal
from typing import Awaitable, Callable, Optional

from cubes.buffer import Buffer
from cubes.connection import CloseConnection, Connection, ConnectionStatus

log = logging.getLogger(__name__)


class GracefulExit(SystemExit):
    pass


async def _default_unhandled_packet_handler(packet: Buffer) -> None:
    conn = Connection.get_current()
    packet.reset_pos()
    log.debug(
        "Handler for packet id %i with state %s not implemented.",
        packet.unpack_varint(),
        conn.state.name,
    )


class Server:
    _handlers: dict[tuple[ConnectionStatus, int], Awaitable]
    _unhandled_packet_handler: Awaitable

    def __init__(self, host: str, port: int):
        self._host, self._port = host, port
        self._handlers = {}
        self._unhandled_packet_handler = _default_unhandled_packet_handler

    def run(self) -> None:
        loop = asyncio.get_event_loop()
        try:
            loop.add_signal_handler(signal.SIGINT, self._raise_graceful_exit)
            loop.add_signal_handler(signal.SIGTERM, self._raise_graceful_exit)
        except NotImplementedError:  # signals not implemented on windows
            pass
        log.info("Starting server on %s:%i", self._host, self._port)
        try:
            loop.run_until_complete(self._run())
        except (GracefulExit, KeyboardInterrupt):
            pass
        finally:
            log.info("Server stopped")

    def add_low_level_handler(
        self, conn_status: ConnectionStatus, packet_id: int, func: Callable
    ) -> None:
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
        except Exception as e:
            log.exception(e)
            raise GracefulExit

    async def _accept_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        conn = Connection(reader, writer)
        conn.set_current()
        try:
            while True:
                packet = await conn.read_packet()
                if not packet:
                    return
                await self._process_packet(conn, packet)
        except CloseConnection:
            log.debug("Connection closed by packet handler.")
        finally:
            await conn.close()

    async def _process_packet(self, conn: Connection, packet: Buffer) -> None:
        packet_id = packet.unpack_varint()
        handler = self._handlers.get((conn.status, packet_id))
        handler = handler if handler else self._unhandled_packet_handler
        buffer: Optional[Buffer] = await handler(packet)
        if buffer:
            await conn.send_packet(buffer)
