from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserSchema):
    password: str
    confirm_password: str


class UserUpdate(UserCreate):
    pass
