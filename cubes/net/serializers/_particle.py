import io

from cubes.net.serializers import _abc, _mixins, _simple, _slot, _var_length
from cubes.types_ import particle


class ParticleSerializer(
    _mixins.BufferSerializeMixin[particle.Particle],
    _abc.AbstractSerializer[particle.Particle],
):
    @classmethod
    def validate(cls, value: particle.Particle) -> None:
        """"""

    @classmethod
    def deserialize(cls, data: bytes) -> particle.Particle:
        return cls.from_buffer(io.BytesIO(data))

    def to_buffer(self, buffer: io.BytesIO) -> None:
        _var_length.VarIntSerializer(self._value.id, validate=False).to_buffer(buffer)
        match self._value.id:
            case particle.ParticleID.BLOCK | particle.ParticleID.FALLING_DUST:
                _var_length.VarIntSerializer(self._value.block_state).to_buffer(buffer)
            case particle.ParticleID.DUST:
                value: particle.DustParticle = self._value
                _simple.FloatSerializer(value.red, validate=False).to_buffer(buffer)
                _simple.FloatSerializer(value.green, validate=False).to_buffer(buffer)
                _simple.FloatSerializer(value.blue, validate=False).to_buffer(buffer)
                _simple.FloatSerializer(value.scale, validate=False).to_buffer(buffer)
            case particle.ParticleID.DUST_COLOR_TRANSITION:
                value: particle.DustColorTransitionParticle = self._value
                _simple.FloatSerializer(value.from_red, validate=False).to_buffer(
                    buffer
                )
                _simple.FloatSerializer(value.from_green, validate=False).to_buffer(
                    buffer
                )
                _simple.FloatSerializer(value.from_blue, validate=False).to_buffer(
                    buffer
                )
                _simple.FloatSerializer(value.scale, validate=False).to_buffer(buffer)
                _simple.FloatSerializer(value.to_red, validate=False).to_buffer(buffer)
                _simple.FloatSerializer(value.to_green, validate=False).to_buffer(
                    buffer
                )
                _simple.FloatSerializer(value.to_blue, validate=False).to_buffer(buffer)
            case particle.ParticleID.ITEM:
                _slot.SlotSerializer(self._value.item, validate=False).to_buffer(buffer)
            case particle.ParticleID.VIBRATION:
                value: particle.VibrationParticle = self._value
                _simple.DoubleSerializer(value.origin_x, validate=False).to_buffer(
                    buffer
                )
                _simple.DoubleSerializer(value.origin_y, validate=False).to_buffer(
                    buffer
                )
                _simple.DoubleSerializer(value.origin_z, validate=False).to_buffer(
                    buffer
                )
                _simple.DoubleSerializer(value.dest_x, validate=False).to_buffer(buffer)
                _simple.DoubleSerializer(value.dest_y, validate=False).to_buffer(buffer)
                _simple.DoubleSerializer(value.dest_z, validate=False).to_buffer(buffer)
                _simple.IntSerializer(value.ticks, validate=False).to_buffer(buffer)

    @classmethod
    def from_buffer(cls, buffer: io.BytesIO) -> particle.Particle:
        particle_id = particle.ParticleID(
            _var_length.VarIntSerializer.from_buffer(buffer)
        )
        match particle_id:
            case particle.ParticleID.BLOCK:
                result = particle.BlockParticle(
                    _var_length.VarIntSerializer.from_buffer(buffer)
                )
            case particle.ParticleID.DUST:
                result = particle.DustParticle(
                    *[_simple.FloatSerializer.from_buffer(buffer) for _ in range(4)]
                )
            case particle.ParticleID.DUST_COLOR_TRANSITION:
                from_colors = [
                    _simple.FloatSerializer.from_buffer(buffer) for _ in range(3)
                ]
                scale = _simple.FloatSerializer.from_buffer(buffer)
                result = particle.DustColorTransitionParticle(
                    *from_colors,
                    *[_simple.FloatSerializer.from_buffer(buffer) for _ in range(3)],
                    scale,
                )
            case particle.ParticleID.FALLING_DUST:
                result = particle.FallingDustParticle(
                    _var_length.VarIntSerializer.from_buffer(buffer)
                )
            case particle.ParticleID.ITEM:
                result = particle.ItemParticle(_slot.SlotSerializer.from_buffer(buffer))
            case particle.ParticleID.VIBRATION:
                result = particle.VibrationParticle(
                    *[_simple.DoubleSerializer.from_buffer(buffer) for _ in range(6)],
                    _simple.IntSerializer.from_buffer(buffer),
                )
            case _:
                result = particle.Particle(particle_id)
        return result
