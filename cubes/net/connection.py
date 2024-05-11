import io
from typing import cast

import anyio
import anyio.abc

from cubes.net import serializers


class _LengthVarIntSerializer(serializers.VarIntSerializer):
    _MAX_BYTES = 3
    _RANGE = (1, 2097151)


class Connection:
    __slots__ = ("_stream", "_remote_address", "_local_address", "_state")

    def __init__(self, stream: anyio.abc.SocketStream):
        self._stream = stream
        self._remote_address = cast(
            anyio.abc.IPSockAddrType,
            stream.extra(anyio.abc.SocketAttribute.remote_address),
        )
        self._local_address = cast(
            anyio.abc.IPSockAddrType,
            stream.extra(anyio.abc.SocketAttribute.local_address),
        )

    @property
    def remote_address(self) -> anyio.abc.IPSockAddrType:
        return self._remote_address

    @property
    def local_address(self) -> anyio.abc.IPSockAddrType:
        return self._local_address

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
