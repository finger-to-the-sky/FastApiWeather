from app.auth.utils.auth_operations import get_token_data
from app.users.schemas import User


def check_user_permissions(token: str) -> bool:
    data = get_token_data(token)
    if data['is_admin'] or data['is_superuser']:
        return True
    return False


def check_user_permissions_update_or_delete(token: str, user: User) -> bool:
    data = get_token_data(token)
    if data['is_admin'] or data['is_superuser']:
        return True
    else:
        if data['sub'].strip() == str(user.id):
            return True
        return False
