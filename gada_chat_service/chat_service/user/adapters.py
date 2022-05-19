from typing import Optional

from gada_chat_service.core.getstream.constant import UserType
from gada_chat_service.core.user.models import UserDomain
from gada_chat_service.core.user.ports import IUserServiceProvider


class UserServiceProvider(IUserServiceProvider):
    def __init__(self):
        self.data = "asd"

    def get_user_marketplace_detail(self, identity: str, is_seller: bool) -> Optional[UserDomain]:
        return UserDomain(
            1,"dejan","asd",UserType.BUYER,"asd","asd"
        )