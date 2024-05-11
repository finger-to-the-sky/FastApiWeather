from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils.users_operations import oauth2_scheme
from app.db.config import DB
from app.users.permissions import check_user_permission_on_superuser, check_user_permissions
from app.users.queries import crud
from app.users.schemas import AdminCreate, SuperUserCreate, UserCreate

router = APIRouter(tags=['Users Management'], prefix='/users_management')


async def clear_users_list(
        ignore_admin: bool,
        ignore_superuser: bool,
        session: AsyncSession = Depends(DB.session_dependency)
):
    users_list = await crud.get_users(session)
    for user in users_list:
        if ignore_admin is True and user.is_admin == ignore_admin:
            continue
        elif ignore_superuser is True and user.is_superuser == ignore_superuser:
            continue
        else:
            await crud.delete_user(session=session, user=user)


@router.post('/create_users/', status_code=status.HTTP_201_CREATED)
async def create_users(count_users: int,
                       token: str = Depends(oauth2_scheme),
                       session: AsyncSession = Depends(DB.session_dependency)
                       ):
    if check_user_permissions(token):
        for u in range(count_users):
            await crud.create_user(session=session,
                                   user=UserCreate(
                                       email=f'email_{u}@example.com',
                                       username=f'user_{u}',
                                       password=f'password_{u}',
                                       confirm_password=f'password_{u}',
                                   ))
        return {'msg': f"{count_users} new users has been created"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')


@router.post('/create_admin/', status_code=status.HTTP_201_CREATED)
async def create_admin(admin_create: AdminCreate,
                       token: str = Depends(oauth2_scheme),
                       session: AsyncSession = Depends(DB.session_dependency)
                       ):
    if check_user_permission_on_superuser(token):
        admin = await crud.get_user_by_username(
            session=session,
            username=admin_create.username
        )
        if admin:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Admin has been created')
        await crud.create_user(session=session,
                               user=admin_create)
        return {'msg': f"Admin has been created successful!", 'user': admin}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')


@router.post('/create_superuser/', status_code=status.HTTP_201_CREATED)
async def create_superuser(superuser_create: SuperUserCreate, session: AsyncSession = Depends(DB.session_dependency)):
    superuser = await crud.get_user_by_username(
        session=session,
        username=superuser_create.username
    )
    if superuser:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail='Superuser has been created'
                             )
    await crud.create_user(session=session,
                           user=superuser_create)
    return {'msg': f"Superuser has been created successful!", 'user': superuser_create}


@router.delete('/clear_users/')
async def clear_users(ignore_admin: bool = False,
                      ignore_superuser: bool = False,
                      token: str = Depends(oauth2_scheme),
                      session: AsyncSession = Depends(DB.session_dependency)
                      ):
    if check_user_permission_on_superuser(token):
        await clear_users_list(ignore_admin=ignore_admin, ignore_superuser=ignore_superuser, session=session)
        return {'msg': 'Users has been deleted!'}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
