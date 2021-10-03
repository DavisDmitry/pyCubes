import uuid

from cubes import utils


def test_generate_uuid():
    assert isinstance(utils.generate_uuid("_Smesharik_"), uuid.UUID)
