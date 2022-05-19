from enum import Enum


class TargetType(Enum):
    BUYER = "BUYER"
    SELLER = "SELLER"


class OrderType(Enum):
    UNREAD = "UNREAD"
    LATEST = "LATEST"


SELLER_INDEX = 1
BUYER_INDEX = 0

SELLER_NAME_STREAM_KEY = "seller_name"
BUYER_NAME_STREAM_KEY = "buyer_name"