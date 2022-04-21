from dataclasses import dataclass


@dataclass
class InsertChannelSpec:
    buyer_getstream_id: str
    seller_getstream_id: str
    channel_id: str
    channel_name: str


@dataclass
class CreateChannelSpec:
    buyer_getstream_id: str
    seller_username: str


@dataclass
class GetChannelSpec:
    getstream_id: str
    target_username: str


@dataclass
class GetChannelDbSpec:
    buyer_getstream_id: str
    seller_getstream_id: str
