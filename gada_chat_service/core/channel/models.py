from dataclasses import dataclass


@dataclass
class ChannelDomain:
    id: str
    buyer_id: str
    seller_id: str
    