import enum
import io

import anyio
import anyio.abc

from cubes.net import serializers


class _LengthVarIntSerializer(serializers.VarIntSerializer):
    _MAX_BYTES = 3
    _RANGE = (1, 2097151)


class ConnectionStatus(enum.IntEnum):
    HANDSHAKE = 0
    STATUS = 1
    LOGIN = 2
    PLAY = 3


class Connection:
    __slots__ = ("_stream", "_remote_address", "_local_address", "_status")

    def __init__(self, stream: anyio.abc.SocketStream):
        self._stream = stream
        self._remote_address = stream.extra(anyio.abc.SocketAttribute.remote_address)
        self._local_address = stream.extra(anyio.abc.SocketAttribute.local_address)
        self._status = ConnectionStatus.HANDSHAKE

    @property
    def status(self) -> ConnectionStatus:
        return self._status

    @property
    def remote_address(self) -> tuple[str, int]:
        return self._remote_address

    @property
    def local_address(self) -> tuple[str, int]:
        return self._local_address

    @status.setter
    def status(self, value: ConnectionStatus):
        self._status = value

    async def receive(self) -> io.BytesIO:
        length = await _LengthVarIntSerializer.from_stream(self._stream)
        return io.BytesIO(await self._stream.receive(length))

    async def send(self, *packets: io.BytesIO) -> None:
        buffer = io.BytesIO()
        for packet in packets:
            _LengthVarIntSerializer(packet.getbuffer().nbytes).to_buffer(buffer)
            buffer.write(packet.getvalue())
        await self._stream.send(buffer.getvalue())

    async def close(self) -> None:
        await self._stream.aclose()
