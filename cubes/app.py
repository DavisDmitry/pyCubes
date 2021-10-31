import asyncio
import logging
import signal
from typing import Callable, Coroutine

from cubes import abc, buffer, connection, types

log = logging.getLogger(__name__)


async def _default_unhandled_packet_handler(packet_id: int, packet: buffer.ReadBuffer):
    log.debug(
        "Handler for packet id %s and state %s not implemented.",
        hex(packet_id),
        packet.connection.status.name,
    )


class GracefulExit(SystemExit):
    """Exception raising when server should stop."""


class Application(abc.Application):
    """Class for creating Minecraft Java Edition server implemetation."""

    # pylint: disable=W0201

    _handlers: dict[
        tuple[types.ConnectionStatus, int],
        Callable[[int, abc.AbstractReadBuffer], Coroutine],
    ]

    def __init__(self, packet_read_timeout: int = 20, process_packet_timeout: int = 20):
        self._packet_read_timeout = packet_read_timeout
        self._process_packet_timeout = process_packet_timeout
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
        self,
        conn_status: types.ConnectionStatus,
        packet_id: int,
        func: Callable[[int, abc.AbstractReadBuffer], Coroutine],
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

    def _change_unhandled_packet_handler(
        self, func: Callable[[int, abc.AbstractReadBuffer], Coroutine]
    ) -> None:
        self._unhandled_packet_handler = func

    unhandled_packet_handler = property(fset=_change_unhandled_packet_handler)

    @staticmethod
    def _raise_graceful_exit() -> None:
        raise GracefulExit

    async def _run(self, host: str, port: int) -> None:
        try:
            server = await asyncio.start_server(self._accept_connection, host, port)
            async with server:
                await server.serve_forever()
        except Exception as exc:
            log.exception(exc)
            raise GracefulExit from exc

    async def _accept_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        # pylint: disable=W0703
        reason = None
        conn = connection.PlayerConnection(reader, writer, self)
        try:
            while not conn.is_closing:
                packet = await asyncio.wait_for(
                    self._wait_packet(conn), self._packet_read_timeout
                )
                await asyncio.wait_for(
                    self._process_packet(packet), self._process_packet_timeout
                )
        except asyncio.TimeoutError:
            log.debug("Connection (%s, %i) timed out.", *conn.peername)
        except connection.CloseConnection as exc:
            reason = exc.reason
            log.debug("Connection closed by handler. Reason: %s", exc.reason)
        except Exception as exc:
            log.exception(exc)
        finally:
            if not conn.is_closing:
                await conn.close(reason)

    @staticmethod
    async def _wait_packet(conn: connection.PlayerConnection) -> abc.AbstractReadBuffer:
        packet = await conn.read_packet()
        while not packet:
            await asyncio.sleep(0.001)
            packet = await conn.read_packet()
        return packet

    async def _process_packet(self, packet: abc.AbstractReadBuffer) -> None:
        # pylint: disable=W0703
        packet_id = packet.varint
        handler = self._handlers.get((packet.connection.status, packet_id))
        handler = handler if handler else self._unhandled_packet_handler
        try:
            await handler(packet_id, packet)
        except connection.CloseConnection:
            raise
        except Exception as exc:
            log.exception(exc)
