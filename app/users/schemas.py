from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserSchema):
    password: str
    confirm_password: str


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserUpdate):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None
    confirm_password: str | None = None


class User(UserSchema):
    model_config = ConfigDict(from_attributes=True)
    uuid: str
