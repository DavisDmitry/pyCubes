import asyncio
import json
import uuid
from typing import Optional

from cubes import abc
from cubes import buffer as _buffer
from cubes import types_


class CloseConnection(Exception):
    """Raising when connection should be closed."""

    def __init__(self, reason: Optional[str] = None):
        super().__init__(reason)
        self.reason = reason


class DisconnectedByServerError(Exception):
    """Raising when server sends disconnect packet."""

    def __init__(self, state: types_.ConnectionStatus, reason: str) -> None:
        super().__init__(f"State: {state.name}, reason: {reason}.")


class UnexpectedPacketError(Exception):
    """Raising when server sends unexpected packet."""

    def __init__(self, packet_id: int) -> None:
        super().__init__(f"Packet ID: {hex(packet_id)}")


class InvalidPlayerNameError(Exception):
    """Raising when server sent Login Success packet with invalid player name."""

    def __init__(self, valid_name: str, invalid_name: str) -> None:
        super().__init__(f"{valid_name} != {invalid_name}")


class _BaseConnection:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._reader, self._writer = reader, writer

    async def read_packet(self) -> Optional[abc.AbstractReadBuffer]:
        """Reads a packet."""
        try:
            return await _buffer.ReadBuffer.from_reader(self, self._reader)
        except _buffer.EmptyBufferError:
            pass

    async def wait_packet(self) -> abc.AbstractReadBuffer:
        """Waits and reads a packet."""
        packet = await self.read_packet()
        while not packet:
            await asyncio.sleep(0.001)
            packet = await self.read_packet()
        return packet

    async def send_packet(self, buffer: abc.AbstractWriteBuffer) -> None:
        """Sends packet."""
        self._writer.write(buffer.packed)
        await self._writer.drain()


class PlayerConnection(_BaseConnection, abc.AbstractPlayerConnection):
    """Player-to-server connection.

    Attributes:
        status (cubes.ConnectionStatus): Connection status.
    """

    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        app: abc.Application,
    ):
        super().__init__(reader, writer)
        self._app = app
        self.status = types_.ConnectionStatus.HANDSHAKE

    async def close(self, reason: Optional[str] = None) -> None:
        """Closes connection."""
        if reason:
            reason = json.dumps({"text": reason})
            if self.status == types_.ConnectionStatus.LOGIN:
                await self.send_packet(
                    _buffer.WriteBuffer().pack_varint(0x00).pack_string(reason)
                )
            if self.status == types_.ConnectionStatus.PLAY:
                await self.send_packet(
                    _buffer.WriteBuffer().pack_varint(0x1A).pack_string(reason)
                )
        self._writer.close()
        await self._writer.wait_closed()


class ClientConnection(_BaseConnection, abc.AbstractClientConnection):
    """Client connection.

    Attributes:
        status (cubes.ConnectionStatus): Connection status
    """

    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        player: types_.PlayerData,
    ):
        super().__init__(reader, writer)
        self._player = player
        self.status = types_.ConnectionStatus.PLAY

    @classmethod
    async def connect(
        cls, host: str, port: int, protocol: int, player_name: str
    ) -> abc.AbstractClientConnection:
        reader, writer = await asyncio.open_connection(host, port)
        conn = cls(reader, writer, None)
        await conn.send_packet(
            _buffer.WriteBuffer(b"\x00")
            .pack_varint(protocol)
            .pack_string(host)
            .pack_unsigned_short(port)
            .write(b"\x02")
        )
        await conn.send_packet(_buffer.WriteBuffer(b"\x00").pack_string(player_name))
        packet = await conn.wait_packet()
        packet_id = packet.varint
        if packet_id == 0x00:
            raise DisconnectedByServerError(
                types_.ConnectionStatus.LOGIN, packet.string
            )
        if packet_id != 0x02:
            raise UnexpectedPacketError(packet_id)
        player = types_.PlayerData(uuid.UUID(bytes=packet.read(16)), packet.string)
        if player_name != player.name:
            raise InvalidPlayerNameError(player_name, player.name)
        return cls(reader, writer, player)

    async def close(self) -> None:
        """Closes connection."""
        self._writer.close()
        await self._writer.wait_closed()
