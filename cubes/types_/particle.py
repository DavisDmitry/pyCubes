import enum
from typing import Optional

import pydantic

from cubes.types_ import slot

_MAX_STATES_VALUE = 9  # composter has 9 states

# pylint: disable=W0231,W0233


class ParticleID(enum.IntEnum):
    AMBIENT_ENTITY_EFFECT = 0
    ANGRY_VILLAGER = 1
    BARRIER = 2
    LIGHT = 3
    BLOCK = 4
    BUBBLE = 5
    CLOUD = 6
    CRIT = 7
    DAMAGE_INDICATOR = 8
    DRAGON_BREATHE = 9
    DRIPPING_LAVA = 10
    FALLING_LAVA = 11
    LANDING_LAVA = 12
    DRIPPING_WATER = 13
    FALLING_WATER = 14
    DUST = 15
    DUST_COLOR_TRANSITION = 16
    EFFECT = 17
    ELDER_GUARDIAN = 18
    ENCHANTED_HIT = 19
    ENCHANT = 20
    END_ROD = 21
    ENTITY_EFFECT = 22
    EXPLOSION_EMMITER = 23
    EXPLOSION = 24
    FALLING_DUST = 25
    FIREWORK = 26
    FISHING = 27
    FLAME = 28
    SOUL_FIRE_FLAME = 29
    SOUL = 30
    FLASH = 31
    HAPPY_VILLAGER = 32
    COMPOSTER = 33
    HEART = 34
    INSTANT_EFFECT = 35
    ITEM = 36
    VIBRATION = 37
    ITEM_SLIME = 38
    ITEM_SNOWBALL = 39
    LARGE_SMOKE = 40
    LAVA = 41
    MYCELIUM = 42
    NOTE = 43
    POOF = 44
    PORTAL = 45
    RAIN = 46
    SMOKE = 47
    SNEEZE = 48
    SPIT = 49
    SQUID_INK = 50
    SWEEP_ATTACK = 51
    TOTEM_OF_UNDYING = 52
    UNDERWATER = 53
    SPLASH = 54
    WITCH = 55
    BUBBLE_POP = 56
    CURRENT_DOWN = 57
    BUBBLE_COLUMN_UP = 58
    NAUTILUS = 59
    DOLPHIN = 60
    CAMPFIRE_COSY_SMOKE = 61
    CAMPFIRE_SIGNAL_SMOKE = 62
    DRIPPING_HONEY = 63
    FALLING_HONEY = 64
    LANDING_HONEY = 65
    FALLING_NECTAR = 66
    FALLING_SPORE_BLOSSOM = 67
    ASH = 68
    CRIMSON_SPORE = 69
    WARPED_SPORE = 70
    SPORE_BLOSSOM_AIR = 71
    DRIPPING_OBSIDIAN_TEAR = 72
    FALLING_OBSIDIAN_TEAR = 73
    LANDING_OBSIDIAN_TEAR = 74
    REVERSE_PORTAL = 75
    WHITE_ASH = 76
    SMALL_FLAME = 77
    SNOWFLAKE = 78
    DRIPPING_DRIPSTONE_LAVA = 79
    FALLING_DRIPSTONE_LAVA = 80
    DRIPPING_DRIPSTONE_WATER = 81
    FALLING_DRIPSTONE_WATER = 82
    GLOW_SQUID_INK = 83
    GLOW = 84
    WAX_ON = 85
    WAX_OFF = 86
    ELECTRIC_SPARK = 87
    SCRAPE = 88

    @property
    def identifier(self) -> str:
        return f"minecraft:{self.name.lower()}"


class Particle(pydantic.BaseModel):
    # pylint: disable=R0903
    id: ParticleID

    def __init__(self, _id: ParticleID):
        super().__init__(id=_id)

    @pydantic.validator("id")
    @classmethod
    def _validate_id(cls, value: ParticleID):
        if value not in (
            ParticleID.BLOCK,
            ParticleID.DUST,
            ParticleID.DUST_COLOR_TRANSITION,
            ParticleID.FALLING_DUST,
            ParticleID.ITEM,
            ParticleID.VIBRATION,
        ):
            return value
        class_name = f"{value.name.title().replace('_', '')}Particle"
        if class_name != cls.__name__:
            raise ValueError
        return value

    class Config:
        allow_mutation = False


class BlockParticle(Particle):
    block_state: int = pydantic.Field(ge=0, le=_MAX_STATES_VALUE)

    def __init__(self, block_state: int):
        pydantic.BaseModel.__init__(self, id=ParticleID.BLOCK, block_state=block_state)


class DustParticle(Particle):
    red: float = pydantic.Field(ge=0, le=1)
    green: float = pydantic.Field(ge=0, le=1)
    blue: float = pydantic.Field(ge=0, le=1)
    scale: float = pydantic.Field(ge=0.01, le=4)

    def __init__(self, red: float, green: float, blue: float, scale: float):
        pydantic.BaseModel.__init__(
            self, id=ParticleID.DUST, red=red, green=green, blue=blue, scale=scale
        )


class DustColorTransitionParticle(Particle):
    from_red: float = pydantic.Field(ge=0, le=1)
    from_green: float = pydantic.Field(ge=0, le=1)
    from_blue: float = pydantic.Field(ge=0, le=1)
    scale: float = pydantic.Field(ge=0.01, le=4)
    to_red: float = pydantic.Field(ge=0, le=1)
    to_green: float = pydantic.Field(ge=0, le=1)
    to_blue: float = pydantic.Field(ge=0, le=1)

    def __init__(
        self,
        from_red: float,
        from_green: float,
        from_blue: float,
        to_red: float,
        to_green: float,
        to_blue: float,
        scale: float,
    ):
        # pylint: disable=R0913
        pydantic.BaseModel.__init__(
            self,
            id=ParticleID.DUST_COLOR_TRANSITION,
            from_red=from_red,
            from_green=from_green,
            from_blue=from_blue,
            scale=scale,
            to_red=to_red,
            to_green=to_green,
            to_blue=to_blue,
        )


class FallingDustParticle(Particle):
    block_state: int = pydantic.Field(ge=0, le=_MAX_STATES_VALUE)

    def __init__(self, block_state: int):
        pydantic.BaseModel.__init__(
            self, id=ParticleID.FALLING_DUST, block_state=block_state
        )


class ItemParticle(Particle):
    item: Optional[slot.Slot]

    def __init__(self, item: slot.Slot | None = None):
        pydantic.BaseModel.__init__(self, id=ParticleID.ITEM, item=item)


class VibrationParticle(Particle):
    origin_x: float
    origin_y: float
    origin_z: float
    dest_x: float
    dest_y: float
    dest_z: float
    ticks: int = pydantic.Field(gt=0)

    def __init__(
        self,
        origin_x: float,
        origin_y: float,
        origin_z: float,
        dest_x: float,
        dest_y: float,
        dest_z: float,
        ticks: int,
    ):
        # pylint: disable=R0913
        pydantic.BaseModel.__init__(
            self,
            id=ParticleID.VIBRATION,
            origin_x=origin_x,
            origin_y=origin_y,
            origin_z=origin_z,
            dest_x=dest_x,
            dest_y=dest_y,
            dest_z=dest_z,
            ticks=ticks,
        )
