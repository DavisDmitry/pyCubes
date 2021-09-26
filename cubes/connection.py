import logging
from asyncio import StreamReader as Reader
from asyncio import StreamWriter as Writer
from contextvars import ContextVar
from enum import IntEnum
from typing import Optional

from cubes.buffer import Buffer, EmptyBuffer

_CONNECTION = ContextVar(__name__)


log = logging.getLogger(__name__)


class CloseConnection(Exception):
    pass


class ConnectionStatus(IntEnum):
    HANDSHAKE = 0
    STATUS = 1
    LOGIN = 2
    PLAY = 3


class Connection:
    def __init__(self, reader: Reader, writer: Writer):
        self._reader, self._writer = reader, writer
        self.status, self._threshold = ConnectionStatus.HANDSHAKE, 0

    @classmethod
    def get_current(cls) -> Optional["Connection"]:
        return _CONNECTION.get()

    def set_current(self) -> None:
        _CONNECTION.set(self)

    async def close(self) -> None:
        self._writer.close()
        await self._writer.wait_closed()

    async def read_packet(self) -> Optional[Buffer]:
        try:
            return await Buffer.from_reader(self._reader)
        except EmptyBuffer:
            log.debug("Client sent empty packet.")

    async def send_packet(self, buffer: Buffer) -> None:
        self._writer.write(buffer.packed)
        await self._writer.drain()
