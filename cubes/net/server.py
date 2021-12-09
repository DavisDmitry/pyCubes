import io
from typing import Any, Callable, Coroutine

import anyio
import anyio.abc

from cubes.net import connection


class Server:
    __slots__ = (
        "_new_connection_handler",
        "_packet_receive_timeout_handler",
        "_process_packet_handler",
        "_close_connection_handler",
        "_packet_receive_timeout",
        "_is_running",
    )

    def __init__(
        self,
        new_connection_handler: Callable[
            [connection.Connection], Coroutine[Any, Any, None]
        ],
        packet_receive_timeout_handler: Callable[
            [connection.Connection], Coroutine[Any, Any, None]
        ],
        process_packet_handler: Callable[
            [connection.Connection, io.BytesIO], Coroutine[Any, Any, None]
        ],
        close_connection_handler: Callable[
            [connection.Connection, Exception], Coroutine[Any, Any, None]
        ],
        packet_receive_timeout: float = 20,
    ):
        # pylint: disable=R0913
        self._new_connection_handler = new_connection_handler
        self._packet_receive_timeout_handler = packet_receive_timeout_handler
        self._process_packet_handler = process_packet_handler
        self._packet_receive_timeout = packet_receive_timeout
        self._close_connection_handler = close_connection_handler
        self._is_running = False

    @property
    def is_running(self) -> bool:
        return self._is_running

    async def _process_packet(self, conn: connection.Connection) -> None:
        try:
            with anyio.fail_after(self._packet_receive_timeout):
                packet = await conn.receive()
        except TimeoutError:
            await self._packet_receive_timeout_handler(conn)
            return
        await self._process_packet_handler(conn, packet)

    async def _process_packets(self, conn: connection.Connection) -> None:
        while True:
            await self._process_packet(conn)

    async def _accept_connection(self, stream: anyio.abc.SocketStream) -> None:
        # pylint: disable=W0703
        reason = None
        try:
            async with stream:
                conn = connection.Connection(stream)
                await self._new_connection_handler(conn)
                await self._process_packets(conn)
        except Exception as exc:
            reason = exc
        finally:
            await self._close_connection_handler(conn, reason)

    async def run(
        self,
        host: str,
        port: int,
        *,
        task_status: anyio.abc.TaskStatus = anyio.TASK_STATUS_IGNORED,
    ) -> None:
        listener = await anyio.create_tcp_listener(local_host=host, local_port=port)
        self._is_running = True
        try:
            task_status.started()
            await listener.serve(self._accept_connection)
        finally:
            await listener.aclose()
