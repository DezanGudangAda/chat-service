from abc import ABC, abstractmethod
from typing import Optional

from gada_chat_service.core.user.models import UserDomain


class IUserServiceProvider(ABC):
    @abstractmethod
    def get_user_marketplace_detail(self, identity: str, is_seller: bool) -> Optional[UserDomain]:
        raise NotImplementedError