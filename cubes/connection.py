import asyncio
import json
from typing import Optional

from cubes import abc, buffer, types


class CloseConnection(Exception):
    """Raising when connection should be closed."""

    def __init__(self, reason: Optional[str] = None):
        if reason:
            super().__init__(reason)
            self.reason = reason
        else:
            super().__init__()


class Connection(abc.AbstractConnection):
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
        super().__init__(reader, writer, app)
        self.status = types.ConnectionStatus.HANDSHAKE

    async def close(self, reason: Optional[str] = None) -> None:
        """Closes connection."""
        if reason:
            reason = json.dumps({"text": reason})
            if self.status == types.ConnectionStatus.LOGIN:
                await self.send_packet(
                    buffer.WriteBuffer().pack_varint(0x00).pack_string(reason)
                )
            if self.status == types.ConnectionStatus.PLAY:
                await self.send_packet(
                    buffer.WriteBuffer().pack_varint(0x1A).pack_string(reason)
                )
        self._writer.close()
        await self._writer.wait_closed()

    async def read_packet(self) -> Optional[abc.AbstractReadBuffer]:
        """Reads packet."""
        try:
            return await buffer.ReadBuffer.from_reader(self, self._reader)
        except buffer.EmptyBufferError:
            pass

    async def send_packet(self, _buffer: abc.AbstractWriteBuffer) -> None:
        """Sends packet."""
        self._writer.write(_buffer.packed)
        await self._writer.drain()
