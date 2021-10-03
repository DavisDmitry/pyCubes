import uuid

# pylint: disable=R0903


def generate_uuid(player_name: str) -> uuid.UUID:
    """Generates UUID by player_name for using in offline mode."""

    class NameSpace:
        # pylint: disable=C0115
        bytes = b"OfflinePlayer"

    return uuid.uuid3(NameSpace, player_name)
