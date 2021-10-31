import asyncio
import json
from typing import Optional

from cubes import abc
from cubes import buffer as _buffer
from cubes import types


class CloseConnection(Exception):
    """Raising when connection should be closed."""

    def __init__(self, reason: Optional[str] = None):
        super().__init__(reason)
        self.reason = reason


class PlayerConnection(abc.AbstractPlayerConnection):
    """Client or server connection.

    Attributes:
        status (cubes.ConnectionStatus): Connection status.
    """

    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        app: abc.Application,
    ):
        self._reader, self._writer, self._app = reader, writer, app
        self.status = types.ConnectionStatus.HANDSHAKE

    async def close(self, reason: Optional[str] = None) -> None:
        """Closes connection."""
        if reason:
            reason = json.dumps({"text": reason})
            if self.status == types.ConnectionStatus.LOGIN:
                await self.send_packet(
                    _buffer.WriteBuffer().pack_varint(0x00).pack_string(reason)
                )
            if self.status == types.ConnectionStatus.PLAY:
                await self.send_packet(
                    _buffer.WriteBuffer().pack_varint(0x1A).pack_string(reason)
                )
        self._writer.close()
        await self._writer.wait_closed()

    async def read_packet(self) -> Optional[abc.AbstractReadBuffer]:
        """Reads packet."""
        try:
            return await _buffer.ReadBuffer.from_reader(self, self._reader)
        except _buffer.EmptyBufferError:
            pass

    async def send_packet(self, buffer: abc.AbstractWriteBuffer) -> None:
        """Sends packet."""
        self._writer.write(buffer.packed)
        await self._writer.drain()
