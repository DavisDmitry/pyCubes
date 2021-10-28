import uuid

# pylint: disable=R0903


def generate_uuid(player_name: str) -> uuid.UUID:
    """Generates UUID by player_name for using in offline mode."""

    class _NameSpace:
        bytes = b"OfflinePlayer:"

    return uuid.uuid3(_NameSpace, player_name)
