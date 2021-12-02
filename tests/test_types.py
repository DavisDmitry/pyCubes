import pydantic
import pytest
from pydantic.class_validators import validator

from cubes import nbt as _nbt
from cubes import types_


@pytest.mark.parametrize(
    ("item_id", "count", "nbt"),
    ((1, 64, None), (719, 1, _nbt.Compound({"Unbreakable": _nbt.Byte(True)}))),
)
def test_valid_slot(item_id: int, count: int, nbt: _nbt.Compound | None):
    value = types_.Slot(item_id, count, nbt=nbt)
    assert value.item_id == item_id
    assert value.count == count
    assert value.nbt == nbt


@pytest.mark.parametrize(
    ("item_id", "count", "nbt"),
    ((-1, 1, None), (1, 0, None), (1, 65, None), (1, 1, "test")),
)
def test_invalid_slot(item_id: int, count: int, nbt: _nbt.Compound | None):
    with pytest.raises(pydantic.ValidationError):
        types_.Slot(item_id, count, nbt=nbt)


def test_slot_mutation():
    new_count, new_nbt = 32, _nbt.Compound({"test": _nbt.String("test")})
    slot = types_.Slot(1, 64)
    with pytest.raises(TypeError):
        slot.item_id = 2
    slot.count = new_count
    slot.nbt = new_nbt
    assert slot.count == new_count
    assert slot.nbt == new_nbt
