from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.config import DB
from app.users import queries
from app.users.queries import crud
from app.users.schemas import UserCreate

router = APIRouter(prefix='/users', tags=['Users'])

fake_user = {
    "email": "username@example.com",
    "username": 'username'
}


@router.get('/all/')
async def get_all_users(session: AsyncSession = Depends(DB.session_dependency)):
    return await crud.get_users(session=session)


@router.get('/id/{user_id}/')
async def get_user_by_id(user_uuid: str, session: AsyncSession = Depends(DB.session_dependency)):
    user = await crud.get_user_by_uuid(session=session, user_id=user_uuid)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User: {user_uuid} not found')


@router.post('/create_user/', status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(DB.session_dependency)):
    if user_create.password != user_create.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Password and Confirm Password does not equal')
    return await crud.create_user(session=session, user=user_create)
