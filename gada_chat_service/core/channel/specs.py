from dataclasses import dataclass

from gada_chat_service.core.getstream.constant import UserType


@dataclass
class InsertChannelSpec:
    buyer_getstream_id: str
    seller_getstream_id: str
    channel_id: str
    channel_name: str


@dataclass
class GetChannelByUsersSpec:
    buyer_getstream_id: str
    seller_getstream_id: str

