import enum

from cubes.types_ import _mixins


class FieldType(enum.IntEnum):
    BYTE = 0
    VARINT = 1
    FLOAT = 2
    STRING = 3
    CHAT = 4
    OPT_CHAT = 5
    SLOT = 6
    BOOLEAN = 7
    ROTATION = 8
    POSITION = 9
    OPT_POSITION = 10
    DIRECTION = 11
    OPT_UUID = 12
    OPT_BLOCK_ID = 13
    NBT = 14
    PARTICLE = 15
    VILLAGER_DATA = 16
    OPT_VARINT = 17
    POSE = 18


class Direction(_mixins.IdentifierMixin, enum.IntEnum):
    DOWN = 0
    UP = 1
    NORTH = 2
    SOUTH = 3
    WEST = 4
    EAST = 5


class VillagerType(_mixins.IdentifierMixin, enum.IntEnum):
    DESERT = 0
    JINGLE = 1
    PLAINS = 2
    SAVANNA = 3
    SNOW = 4
    SWAMP = 5
    TAIGA = 6


class VillagerProfession(_mixins.IdentifierMixin, enum.IntEnum):
    NONE = 0
    ARMORER = 1
    BUTCHER = 2
    CARTOGRAPHER = 3
    CLERIC = 4
    FARMER = 5
    FISHERMAN = 6
    FLETCHER = 7
    LEATHERWORKER = 8
    LIBRARIAN = 9
    MASON = 10
    NITWIT = 11
    SHEPHERD = 12
    TOOLSMITH = 13
    WEAPONSMITH = 14


class Pose(enum.IntEnum):
    STANDING = 0
    FALL_FLYING = 1
    SLEEPING = 2
    SWIMMING = 3
    SPIN_ATTACK = 4
    SNEAKING = 5
    LONG_JUMPING = 5
    DYING = 6
