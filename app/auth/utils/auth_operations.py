from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError

from app.auth.utils.exceptions import raise_401_exception
from app.auth.schemas import TokenData
from app.auth.config import auth_settings

TYPE_FIELD_TOKEN = 'type'
ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'


def create_access_token(user):
    access_token_expires = timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_token_expires
    data = {
        "sub": str(user.id),
        "is_admin": user.is_admin,
        "is_superuser": user.is_superuser,
        "exp": expire,
        TYPE_FIELD_TOKEN: ACCESS_TOKEN_TYPE
    }
    encoded_jwt = jwt.encode(data, auth_settings.PRIVATE_KEY, algorithm=auth_settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(user):
    refresh_token_expires = timedelta(days=auth_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    expire = datetime.now(timezone.utc) + refresh_token_expires
    data = {
        "sub": str(user.id),
        "is_admin": user.is_admin,
        "is_superuser": user.is_superuser,
        "exp": expire,
        TYPE_FIELD_TOKEN: REFRESH_TOKEN_TYPE
    }
    encoded_jwt = jwt.encode(data, auth_settings.PRIVATE_KEY, algorithm=auth_settings.ALGORITHM)
    return encoded_jwt


def validate_type_token(expected_type: str, payload: dict):
    if expected_type == payload.get(TYPE_FIELD_TOKEN):
        return True
    raise raise_401_exception('Token invalid')


def get_token_data(token: str) -> dict | None:
    exc = raise_401_exception("Could not validate credentials")
    try:
        payload = jwt.decode(token, auth_settings.PRIVATE_KEY, algorithms=[auth_settings.ALGORITHM])
        return payload
    except JWTError:
        raise exc


def get_user_from_payload(token: str, token_type: str = ACCESS_TOKEN_TYPE) -> TokenData | None:
    exc = raise_401_exception("Could not validate credentials")
    try:
        payload = get_token_data(token=token)
        validate_type_token(token_type, payload)
        user_id: str = payload.get("sub")
        if user_id:
            return TokenData(id=user_id)
        raise exc
    except JWTError:
        raise exc
