import asyncio
import contextvars as cv
import enum
import logging

from cubes import buffer

_CONNECTION = cv.ContextVar(__name__)


log = logging.getLogger(__name__)


class CloseConnection(Exception):
    """Raising when connection should be closed."""


class ConnectionStatus(enum.IntEnum):
    # pylint: disable=C0115
    HANDSHAKE = 0
    STATUS = 1
    LOGIN = 2
    PLAY = 3


class Connection:
    """Client or server connection."""

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._reader, self._writer = reader, writer
        self.status, self._threshold = ConnectionStatus.HANDSHAKE, 0

    @classmethod
    def get_current(cls) -> "Connection" | None:
        """Returns current `Connection` instance."""
        return _CONNECTION.get()

    def set_current(self) -> None:
        """Sets instance as a current."""
        _CONNECTION.set(self)

    async def close(self) -> None:
        """Closes connection."""
        self._writer.close()
        await self._writer.wait_closed()

    async def read_packet(self) -> buffer.ReadBuffer | None:
        """Reads packet."""
        try:
            return await buffer.ReadBuffer.from_reader(self._reader)
        except buffer.EmptyBufferError:
            log.debug("Client sent empty packet.")

    async def send_packet(self, _buffer: buffer.WriteBuffer) -> None:
        """Sends packet."""
        self._writer.write(_buffer.packed)
        await self._writer.drain()
