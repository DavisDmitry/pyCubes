import asyncio
import json
import logging

import cubes
import cubes.utils

_CURRRENT_PROTOCOL_VERSION = 756


log = logging.getLogger(__name__)


async def process_handshake(_, packet: cubes.ReadBuffer):
    protocol = packet.varint
    packet.string
    packet.unsigned_short
    packet.connection.status = intention = cubes.ConnectionStatus(packet.varint)
    if (
        intention == cubes.ConnectionStatus.LOGIN
        and protocol != _CURRRENT_PROTOCOL_VERSION
    ):
        log.warning("Protocol version %i not implemented.", protocol)
        raise cubes.CloseConnection


async def process_legacy_ping(*_):
    log.warning("Legacy ping not implemeted")
    raise cubes.CloseConnection


async def process_status(_, packet: cubes.ReadBuffer):
    await packet.connection.send_packet(
        cubes.WriteBuffer()
        .pack_varint(0x00)
        .pack_string(
            json.dumps(
                {
                    "version": {
                        "name": "1.17.1",
                        "protocol": _CURRRENT_PROTOCOL_VERSION,
                    },
                    "players": {"max": 0, "online": 0},
                    "description": {"text": "Test Server"},
                }
            )
        )
    )


async def process_status_ping(_, packet: cubes.ReadBuffer):
    await packet.connection.send_packet(
        cubes.WriteBuffer().pack_varint(0x01).write(packet.read(8))
    )


async def process_login_start(_, packet: cubes.ReadBuffer):
    player_name = packet.string
    log.info("Player %s trying to login", player_name)
    uuid = cubes.utils.generate_uuid(player_name)
    packet.connection.status = cubes.ConnectionStatus.PLAY
    await asyncio.sleep(5)
    await packet.connection.send_packet(
        cubes.WriteBuffer().pack_varint(0x02).write(uuid.bytes).pack_string(player_name)
    )
    await asyncio.sleep(5)
    raise cubes.CloseConnection("Playing not implemented")


def main() -> None:
    logging.basicConfig(level="DEBUG")
    app = cubes.Application()

    app.add_low_level_handler(cubes.ConnectionStatus.HANDSHAKE, 0x00, process_handshake)
    app.add_low_level_handler(
        cubes.ConnectionStatus.HANDSHAKE, 0xFE, process_legacy_ping
    )
    app.add_low_level_handler(cubes.ConnectionStatus.STATUS, 0x00, process_status)
    app.add_low_level_handler(cubes.ConnectionStatus.STATUS, 0x01, process_status_ping)
    app.add_low_level_handler(cubes.ConnectionStatus.LOGIN, 0x00, process_login_start)

    app.run("127.0.0.1")


if __name__ == "__main__":
    main()
