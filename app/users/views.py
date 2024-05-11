from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth.utils.users_operations import oauth2_scheme
from app.db.config import DB
from app.users.permissions import check_user_permissions, check_user_permissions_update_or_delete
from app.users.queries import crud, dependecies
from app.users.exceptions import check_user, validate_password
from app.users.schemas import UserCreate, UserUpdate, UserSchema, User, UserUpdatePartial

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/all/', response_model=list[Union[User, UserSchema]])
async def get_all_users(token: str = Depends(oauth2_scheme),
                        session: AsyncSession = Depends(DB.session_dependency)
                        ):
    users = await crud.get_users(session=session)
    if check_user_permissions(token):
        return users
    return [UserSchema(**user.__dict__) for user in users]


@router.post('/create_user/', status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(DB.session_dependency)):
    validate_password(password=user_create.password, confirm_password=user_create.confirm_password)
    return await crud.create_user(session=session, user=user_create)


@router.get('/id/{user_id}/', response_model=Union[User, UserSchema])
async def get_user_by_id(
        token: str = Depends(oauth2_scheme),
        user: Union[User, UserSchema] = Depends(dependecies.user_by_uuid)
):
    if check_user_permissions(token):
        return user
    return UserSchema(username=user.username, email=user.email)


@router.get('/username/{username}/', response_model=Union[User, UserSchema])
async def get_user_by_username(
        username: str,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(DB.session_dependency)
):
    user = await crud.get_user_by_username(session=session, username=username)
    if check_user_permissions(token):
        return await check_user(user=user, data_for_message=username)
    return UserSchema(username=user.username, email=user.email)


@router.get('/email/{email}/', response_model=Union[User, UserSchema])
async def get_user_by_email(
        email: EmailStr,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(DB.session_dependency)
):
    user = await crud.get_user_by_email(session=session, user_email=email)
    if check_user_permissions(token):
        return await check_user(user=user, data_for_message=email)
    return UserSchema(username=user.username, email=user.email)


@router.put('/{user_id}/')
async def update_user(
        user_update: UserUpdate,
        token: str = Depends(oauth2_scheme),
        user: User = Depends(dependecies.user_by_uuid),
        session: AsyncSession = Depends(DB.session_dependency)
):
    if check_user_permissions_update_or_delete(token, user):
        validate_password(password=user_update.password, confirm_password=user_update.confirm_password)
        return await crud.update_user(session=session, user=user, user_update=user_update)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')


@router.patch('/{user_id}/')
async def update_user_partial(
        user_update: UserUpdatePartial,
        token: str = Depends(oauth2_scheme),
        user: User = Depends(dependecies.user_by_uuid),
        session: AsyncSession = Depends(DB.session_dependency)
):
    if check_user_permissions_update_or_delete(token, user):
        validate_password(password=user_update.password, confirm_password=user_update.confirm_password)
        return await crud.update_user(session=session, user=user, user_update=user_update, partial=True)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')


@router.delete('/{user_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        token: str = Depends(oauth2_scheme),
        user: User = Depends(dependecies.user_by_uuid),
        session: AsyncSession = Depends(DB.session_dependency)
) -> None:
    if check_user_permissions_update_or_delete(token, user):
        return await crud.delete_user(session=session, user=user)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
