import io
import uuid
from typing import Any, Callable, Coroutine

import anyio

from cubes import net
from cubes.net import types_

_PROTOCOL = 756
_HOST = "127.0.0.1"
_PORT = 25565
_PLAYER_NAME = "_Smesharik_"


class NotConnectedError(Exception):
    pass


class AlreadyConnectedError(Exception):
    pass


class UnsuitedConnectionStatusForOperationError(Exception):
    pass


class DisconnectedByServerError(Exception):
    pass


class InvalidPlayerNameFromServer(Exception):
    pass


class UnexpectedPacketError(Exception):
    pass


class Client:
    _conn: net.Connection | None

    def __init__(self, host: str, port: int) -> None:
        self._host, self._port = host, port
        self._conn = None

    @property
    def connection(self) -> net.Connection:
        if self._conn is None:
            raise NotConnectedError
        return self._conn

    async def connect(self) -> None:
        if self._conn is not None:
            raise AlreadyConnectedError
        stream = await anyio.connect_tcp(self._host, self._port)
        self._conn = net.Connection(stream)

    async def disconnect(self) -> None:
        await self._conn.close()

    async def login(self, player_name: str) -> uuid.UUID:
        if self.connection.status != net.ConnectionStatus.HANDSHAKE:
            raise UnsuitedConnectionStatusForOperationError(self.connection.status)

        handshake = io.BytesIO()
        types_.VarInt(0x00).to_buffer(handshake)
        types_.VarInt(_PROTOCOL).to_buffer(handshake)
        types_.String(self.connection.remote_address[0])
        types_.UnsignedShort(self.connection.remote_address[1])
        types_.VarInt(net.ConnectionStatus.LOGIN)
        await self.connection.send(handshake)

        self.connection.status = net.ConnectionStatus.LOGIN

        login_start = io.BytesIO()
        types_.VarInt(0x00).to_buffer(login_start)
        types_.String(player_name).to_buffer(login_start)
        await self.connection.send(login_start)

        response = await self.connection.receive()
        packet_id = types_.VarInt.from_buffer(response)
        match packet_id:
            case 0x00:
                raise DisconnectedByServerError(types_.String.from_buffer(response))
            case 0x02:
                uuid_ = types_.UUID.from_buffer(response)
                player_name_from_server = types_.String.from_buffer(response)
                if player_name != player_name_from_server:
                    raise InvalidPlayerNameFromServer(player_name_from_server)
                self.connection.status = net.ConnectionStatus.PLAY
                return uuid_
            case _:
                raise UnexpectedPacketError(hex(packet_id))

    async def run(
        self,
        handler: Callable[[net.Connection, io.BytesIO], Coroutine[Any, Any, None]],
        packet_receive_timeout: float = 20,
    ) -> None:
        while True:
            with anyio.fail_after(packet_receive_timeout):
                packet = await self.connection.receive()
            await handler(self.connection, packet)

    async def __aenter__(self) -> "Client":
        await self.connect()
        return self

    async def __aexit__(self):
        await self.disconnect()


async def process_packet(conn: net.Connection, packet: io.BytesIO):
    ...


async def main():
    async with Client(_HOST, _PORT) as client:
        await client.login(_PLAYER_NAME)
        await client.run(process_packet)
