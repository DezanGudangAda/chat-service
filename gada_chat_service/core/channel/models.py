from dataclasses import dataclass


@dataclass
class ChannelDomain:
    id: str
    buyer_getstream_id: str
    seller_getstream_id: str
    channel_name: str
    