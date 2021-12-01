from typing import Optional

import pydantic

from cubes import nbt as nbt_
from cubes.net.serializers import _nbt, _var_length


class Slot(pydantic.BaseModel):
    item_id: int = pydantic.Field(gt=0, allow_mutation=False)
    count: int = pydantic.Field(gt=0, le=64)
    nbt: Optional[nbt_.Compound]

    def __init__(self, item_id: int, count: int, *, nbt: nbt_.Compound | None = None):
        super().__init__(item_id=item_id, count=count, nbt=nbt)

    @pydantic.validator("item_id")
    @staticmethod
    def _validate_item_id(value: int):
        _var_length.VarIntSerializer.validate(value)

    @pydantic.validator("nbt")
    @staticmethod
    def _validate_nbt(value: nbt_.Compound | None):
        if value is not None:
            _nbt.NBTSerializer.validate(value)

    class Config:
        validate_assignment = True
