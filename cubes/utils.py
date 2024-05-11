import hashlib
import uuid


def generate_uuid(player_name: str) -> uuid.UUID:
    """Generates UUID by player_name for using in offline mode."""
    digest = hashlib.md5(
        b"OfflinePlayer:" + player_name.encode(), usedforsecurity=False
    ).digest()

    return uuid.UUID(bytes=digest[:16], version=3)
