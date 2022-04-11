from dataclasses import dataclass
from typing import Optional, List

from gada_chat_service.core.getstream.constant import UserType, ContextType


@dataclass
class GetUserTokenSpec:
    username: str
    type: UserType


@dataclass
class InsertUserTokenSpec:
    username: str
    type: UserType
    getstream_id: str
    token: str


@dataclass
class ContextSpec:
    related_id: Optional[List[int]]
    type: ContextType


@dataclass
class SendChatSpec:
    message: str
    getstream_id: str
    channel_id: str
    context: Optional[ContextSpec]

