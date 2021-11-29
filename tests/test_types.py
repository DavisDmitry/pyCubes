import uuid

from cubes import types_

_PLAYER_NAME = "_Smesharik_"


def test_player_data():
    player1 = types_.PlayerData(uuid.uuid4(), _PLAYER_NAME)
    player2 = types_.PlayerData(uuid.uuid4(), _PLAYER_NAME)
    assert player1 != player2
    repr(player1)
    repr(player2)
