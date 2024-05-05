from pathlib import Path

from pydantic import BaseModel

CURRENT_DIR = Path(__file__).parent


def get_key(filepath: str | Path) -> bytes:
    with open(filepath, "rb") as key_file:
        key = key_file.read()
        return key


class AuthSettings(BaseModel):
    PRIVATE_KEY_PATH: Path = CURRENT_DIR / 'keys' / 'jwt-private.pem'
    PUBLIC_KEY_PATH: Path = CURRENT_DIR / 'keys' / 'jwt-public.pem'

    PRIVATE_KEY: bytes = get_key(filepath=PRIVATE_KEY_PATH)
    PUBLIC_KEY: bytes = get_key(filepath=PUBLIC_KEY_PATH)
    ALGORITHM: str = 'RS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30


auth_settings = AuthSettings()
