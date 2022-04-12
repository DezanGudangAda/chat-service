from abc import ABC, abstractmethod
from typing import Optional

from gada_chat_service.core.channel.models import ChannelDomain
from gada_chat_service.core.user.models import UserDomain
from gada_chat_service.core.user.specs import GetUserTokenSpec, InsertUserTokenSpec


class IUserAccessor(ABC):
    @abstractmethod
    def get_user_by_username_and_type(self, spec: GetUserTokenSpec) -> Optional[UserDomain]:
        raise NotImplementedError

    @abstractmethod
    def create_user_and_token(self, spec: InsertUserTokenSpec) -> Optional[UserDomain]:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_getstream_id(self, getstream_id: str) -> Optional[UserDomain]:
        raise NotImplementedError
