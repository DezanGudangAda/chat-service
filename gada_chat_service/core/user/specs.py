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
    name: str


@dataclass
class ContextSpec:
    related_id: Optional[List[int]]
    type: ContextType


@dataclass
class SendChatSpec:
    message_code: str
    current_path: str
    identity: str
    role: UserType
    channel_id: str
    context: Optional[ContextSpec]


@dataclass
class ValidateUserReturn:
    is_valid: bool
    details: Optional[str]


@dataclass
class RegisterUserSpec:
    user_type: UserType
    identity: str
    name: str


@dataclass
class GetUnreadChatSpec:
    username: str
    role: UserType


@dataclass
class GetUnreadChatReturn:
    unread_chat: str