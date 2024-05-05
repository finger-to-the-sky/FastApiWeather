from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError

from app.auth.exceptions import raise_401_exception
from app.auth.schemas import TokenData
from app.auth.config import auth_settings


def create_access_token(data: dict,
                        expires_delta: timedelta | None = None
                        ):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, auth_settings.PRIVATE_KEY, algorithm=auth_settings.ALGORITHM)
    return encoded_jwt


def get_token_data(token: str) -> TokenData | None:
    exc = raise_401_exception("Could not validate credentials")
    try:
        payload = jwt.decode(token, auth_settings.PRIVATE_KEY, algorithms=[auth_settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise exc
        token_data = TokenData(id=user_id)
        return token_data
    except JWTError:
        raise exc
