import pydantic
import pytest

from cubes import types_


def test_particle():
    particle_id = types_.ParticleID.ANGRY_VILLAGER
    particle_id.identifier
    assert types_.Particle(particle_id).id == particle_id


def test_invalid_particle():
    with pytest.raises(pydantic.ValidationError):
        types_.Particle(types_.ParticleID.BLOCK)


@pytest.mark.parametrize("block_state", (0, None))
def test_block_particle(block_state: int | None):
    assert types_.BlockParticle(block_state).block_state == block_state


def test_dust_particle():
    values = 139 / 256, 0, 255 / 256, 1  # #8B00FF purple color
    particle = types_.DustParticle(*values)
    assert particle.red == values[0]
    assert particle.green == values[1]
    assert particle.blue == values[2]
    assert particle.scale == values[3]


def test_dust_color_transition():
    values = 139 / 256, 0, 255 / 256, 0, 0, 0, 0.5  # from purple to black
    particle = types_.DustColorTransitionParticle(*values)
    assert particle.from_red == values[0]
    assert particle.from_green == values[1]
    assert particle.from_blue == values[2]
    assert particle.scale == values[-1]
    assert particle.to_red == values[3]
    assert particle.to_green == values[4]
    assert particle.to_blue == values[5]


@pytest.mark.parametrize("block_state", (0, None))
def test_falling_dust_particle(block_state: int | None):
    assert types_.FallingDustParticle(block_state).block_state == block_state


@pytest.mark.parametrize("item", (types_.Slot(1, 64), None))
def test_item_particle(item: types_.Slot | None):
    assert types_.ItemParticle(item).item == item


def test_vibration_particle():
    values = 0, 0, 0, 1, 1, 1, 1
    particle = types_.VibrationParticle(*values)
    assert particle.origin_x == values[0]
    assert particle.origin_y == values[1]
    assert particle.origin_z == values[2]
    assert particle.dest_x == values[3]
    assert particle.dest_y == values[4]
    assert particle.dest_z == values[5]
    assert particle.ticks == values[6]
