from typing import Optional

import pydantic

from cubes import nbt as _nbt


class Slot(pydantic.BaseModel):
    item_id: int = pydantic.Field(gt=0, allow_mutation=False)
    count: int = pydantic.Field(gt=0, le=64)
    nbt: Optional[_nbt.Compound]

    def __init__(
        self, item_id: int, count: int, *, nbt: _nbt.Compound | dict | None = None
    ):
        super().__init__(item_id=item_id, count=count, nbt=nbt)

    @pydantic.validator("nbt")
    @staticmethod
    def validate_nbt(value: _nbt.Compound | None):
        if value is None:
            return value
        return _nbt.Compound(value)

    class Config:
        # pylint: disable=R0903
        validate_assignment = True
