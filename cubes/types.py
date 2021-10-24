import enum


class ConnectionStatus(enum.IntEnum):
    # pylint: disable=C0115
    HANDSHAKE = 0
    STATUS = 1
    LOGIN = 2
    PLAY = 3
