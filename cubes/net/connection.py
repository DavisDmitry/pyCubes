import enum
import io

import anyio
import anyio.abc

from cubes.net import types_


class _LengthVarInt(types_.VarInt):
    _MAX_BYTES = 3
    _RANGE = (1, 2097151)


class ConnectionStatus(enum.IntEnum):
    HANDSHAKE = 0
    STATUS = 1
    LOGIN = 2
    PLAY = 3


class Connection:
    __slots__ = ("_stream", "_status")

    def __init__(self, stream: anyio.abc.SocketStream):
        self._stream = stream
        self._status = ConnectionStatus.HANDSHAKE

    @property
    def status(self) -> ConnectionStatus:
        return self._status

    @property
    def remote_address(self) -> tuple[str, int]:
        return self._stream.extra(anyio.abc.SocketAttribute.remote_address)

    @property
    def local_address(self) -> tuple[str, int]:
        return self._stream.extra(anyio.abc.SocketAttribute.local_address)

    @status.setter
    def status(self, value: ConnectionStatus):
        self._status = value

    async def receive(self) -> io.BytesIO:
        length = await _LengthVarInt.from_stream(self._stream)
        return io.BytesIO(await self._stream.receive(length))

    async def send(self, packet: io.BytesIO) -> None:
        new_packet = io.BytesIO()
        _LengthVarInt(packet.getbuffer().nbytes).to_buffer(new_packet)
        new_packet.write(packet.getvalue())
        await self._stream.send(new_packet.getvalue())

    async def close(self) -> None:
        await self._stream.aclose()
