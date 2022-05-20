import datetime
from dataclasses import dataclass
from typing import Optional, List

from gada_chat_service.core.channel.constants import TargetType, OrderType
from gada_chat_service.core.getstream.constant import UserType


@dataclass
class InsertChannelSpec:
    buyer_getstream_id: str
    seller_getstream_id: str
    channel_id: str
    channel_name: str
    seller_name: str
    buyer_name: str


@dataclass
class CreateChannelSpec:
    buyer_getstream_id: str
    seller_getstream_id: str
    channel_id: str
    channel_name: str
    seller_name: str
    buyer_name: str


@dataclass
class GetChannelSpec:
    username: str
    target: str
    target_type: TargetType


@dataclass
class GetChannelDbSpec:
    buyer_getstream_id: str
    seller_getstream_id: str


@dataclass
class ChannelRoomReturn:
    name: str
    unread_chat: str
    channel_id: str
    date: str
    last_chat: str


@dataclass
class GetChannelListSpec:
    identity: str
    role: UserType
    order: Optional[OrderType]


@dataclass
class GetChannelListReturn:
    chat_rooms: Optional[List[ChannelRoomReturn]]


@dataclass
class SearchChannelSpec:
    role: UserType
    keyword: str
    identity: str


@dataclass
class SearchChannelReturn:
    sender: Optional[List[ChannelRoomReturn]]
    in_chat: Optional[List[ChannelRoomReturn]]