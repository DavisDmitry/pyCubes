import enum


class IdentifierMixin(enum.Enum):
    @property
    def identifier(self) -> str:
        return f"minecraft:{self.name.lower()}"
