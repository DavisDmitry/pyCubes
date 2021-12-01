import pydantic
import pytest

from cubes import nbt as _nbt
from cubes import types_


@pytest.mark.parametrize(
    ("item_id", "count", "nbt"),
    ((1, 64, None), (272, 1, _nbt.Compound({"Unbreakable": _nbt.Byte(True)}))),
)
def test_valid_slot(item_id: int, count: int, nbt: _nbt.Compound | None):
    types_.Slot(item_id, count, nbt=nbt)


@pytest.mark.parametrize(
    ("item_id", "count", "nbt"),
    ((-1, 1, None), (1, 0, None), (1, 65, None), (1, 1, "test")),
)
def test_invalid_slot(item_id: int, count: int, nbt: _nbt.Compound | None):
    with pytest.raises(pydantic.ValidationError):
        types_.Slot(item_id, count, nbt=nbt)


def test_slot_mutation():
    slot = types_.Slot(1, 64)
    with pytest.raises(TypeError):
        slot.item_id = 2
    slot.count = 32
