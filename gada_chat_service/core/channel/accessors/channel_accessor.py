from abc import ABC, abstractmethod
from typing import Optional

from gada_chat_service.core.channel.models import ChannelDomain
from gada_chat_service.core.channel.specs import InsertChannelSpec, GetChannelByUsersSpec


class IChannelAccessor(ABC):
    @abstractmethod
    def get_channel_by_id(self, channel_id: str) -> Optional[ChannelDomain]:
        raise NotImplementedError

    @abstractmethod
    def create_channel(self, spec: InsertChannelSpec) -> Optional[ChannelDomain]:
        raise NotImplementedError

    @abstractmethod
    def get_channel_by_users(self, spec: GetChannelByUsersSpec) -> Optional[ChannelDomain]:
        raise NotImplementedError
