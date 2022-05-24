from dataclasses import dataclass


@dataclass
class ChannelDomain:
    id: str
    buyer_getstream_id: str
    seller_getstream_id: str
    seller_name: str
    buyer_name: str
    