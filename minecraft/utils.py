import uuid


def generate_uuid(player_name: str) -> uuid.UUID:
    class NameSpace:
        bytes = b"OfflinePlayer"

    return uuid.uuid3(NameSpace, player_name)
