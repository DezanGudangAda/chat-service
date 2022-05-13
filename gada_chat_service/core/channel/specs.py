from dataclasses import dataclass

from gada_chat_service.core.channel.constants import TargetType


@dataclass
class InsertChannelSpec:
    buyer_getstream_id: str
    seller_getstream_id: str
    channel_id: str
    channel_name: str


@dataclass
class CreateChannelSpec:
    username: str
    target: str
    target_type: TargetType
    source: str


@dataclass
class GetChannelSpec:
    getstream_id: str
    target_username: str


@dataclass
class GetChannelDbSpec:
    buyer_getstream_id: str
    seller_getstream_id: str
