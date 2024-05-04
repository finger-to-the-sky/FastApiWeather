from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.config import DB
from app.users.queries import crud, dependecies
from app.users.schemas import UserCreate, UserUpdate, UserSchema, User, UserUpdatePartial

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/all/')
async def get_all_users(session: AsyncSession = Depends(DB.session_dependency)):
    return await crud.get_users(session=session)


@router.post('/create_user/', status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(DB.session_dependency)):
    if user_create.password != user_create.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Password and Confirm Password does not equal')
    return await crud.create_user(session=session, user=user_create)


@router.get('/id/{user_id}/')
async def get_user_by_id(user: UserSchema = Depends(dependecies.user_by_uuid)):
    return user


@router.get('/username/{username}/')
async def get_user_by_username(username: str, session: AsyncSession = Depends(DB.session_dependency)):
    user = await crud.get_user_by_username(session=session, username=username)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User {username} not found'
    )


@router.get('/email/{email}/')
async def get_user_by_email(email: str, session: AsyncSession = Depends(DB.session_dependency)):
    user = await crud.get_user_by_email(session=session, user_email=email)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User {email} not found'
    )


@router.put('/{user_id}/')
async def update_user(user_update: UserUpdate,
                      user: User = Depends(dependecies.user_by_uuid),
                      session: AsyncSession = Depends(DB.session_dependency)):
    if user_update.password != user_update.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Password and Confirm Password does not equal')
    return await crud.update_user(session=session, user=user, user_update=user_update, )


@router.patch('/{user_id}/')
async def update_user_partial(user_update: UserUpdatePartial,
                              user: User = Depends(dependecies.user_by_uuid),
                              session: AsyncSession = Depends(DB.session_dependency)):
    if user_update.password != user_update.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Password and Confirm Password does not equal')
    return await crud.update_user(session=session, user=user, user_update=user_update, partial=True)


@router.delete('/{user_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: User = Depends(dependecies.user_by_uuid),
                      session: AsyncSession = Depends(DB.session_dependency)) -> None:
    await crud.delete_user(session=session, user=user)
