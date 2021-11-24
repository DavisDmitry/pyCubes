"""Named Binary Tag.

This module is a wrapper over the [nbtlib](https://github.com/vberlier/nbtlib).
    From it you can use classes: `Byte`, `ByteArray`, `Compound`, `Double`, `End`,
    `Float`, `Int`, `IntArray`, `List`, `Long`, `LongArray`, `Short`, `String`
    and the function `schema`.

Examples:
    >>> cubes.nbt.String('vberlier is cool!')
"""
# pylint: disable=W0611
from nbtlib import (
    Byte,
    ByteArray,
    Compound,
    Double,
    End,
    Float,
    Int,
    IntArray,
    List,
    Long,
    LongArray,
    Short,
    String,
    schema,
)
