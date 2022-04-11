from dataclasses import dataclass

from gada_chat_service.core.getstream.constant import UserType


@dataclass
class InsertChannelSpec:
    buyer_username: str
    seller_username: str
    channel_id: str
    channel_name: str


@dataclass
class GetChannelByUsersSpec:
    buyer_username: str
    seller_username: str

