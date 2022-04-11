from dataclasses import dataclass
from typing import List, Optional

from gada_chat_service.core.getstream.constant import UserType, ContextType


@dataclass
class GenerateUserTokenSpec:
    username: str
    type: UserType


@dataclass
class GenerateUserTokenResult:
    token: str
    stream_id: str


@dataclass
class CreateChannelSpec:
    buyer_getstream_id: str
    seller_getstream_id: str


@dataclass
class CreateChannelResult:
    buyer_getstream_id: str
    seller_getstream_id: str
    channel_name: str
    channel_id: str


@dataclass
class ContextSpec:
    related_id: Optional[List[int]]
    type: ContextType


@dataclass
class ProductAttachmentSpec:
    id: int
    name: str
    current_stock: int
    is_available: bool
    image_url: str
    price: str


@dataclass
class OrderAttachmentSpec:
    order_code: str
    image_url: str
    status: str
    price: str


@dataclass
class ChatMetaSpec:
    sender: str
    getstream_id: str
    need_reply: bool
    channel_id: str
    reply_option: Optional[List[str]]


@dataclass
class ChatExternalDataSpec:
    product_attachment: List[ProductAttachmentSpec]
    order_attachment: Optional[OrderAttachmentSpec]
    chat_meta: Optional[ChatMetaSpec]


@dataclass
class ChatSpec:
    message: str
    product_attachment: List[ProductAttachmentSpec]
    order_attachment: Optional[OrderAttachmentSpec]
    chat_meta: Optional[ChatMetaSpec]
