from typing import Optional, List, Union
from fastapi import APIRouter
from pydantic import BaseModel

from gada_chat_service.chat_service.injector import injector
from gada_chat_service.core.config.services.configuration_service import ConfigurationService
from gada_chat_service.core.getstream.constant import UserType, ContextType
from gada_chat_service.core.user.services.user_services import UserService
from gada_chat_service.core.user.specs import GetUserTokenSpec, SendChatSpec, GetUnreadChatSpec, ContextSpec

user_service: UserService = injector.get(
    UserService
)

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


class ContextRequest(BaseModel):
    related_id: Union[List[int], None] = None
    type: ContextType


class SendingChatRequest(BaseModel):
    message_code: str
    current_path: str
    identity: str
    channel_id: str
    role: UserType
    context: Union[ContextRequest, None] = None


@user_router.post("/chat", tags=["User"])
async def send_message(spec: SendingChatRequest):
    send_message_spec = SendChatSpec(
        channel_id=spec.channel_id,
        message_code=spec.message_code,
        current_path=spec.current_path,
        identity=spec.identity,
        role=spec.role,
        context=None,
    )

    if spec.context is not None:
        context = ContextSpec(
            type=spec.context.type,
            related_id=spec.context.related_id
        )
        send_message_spec.context = context

    res = user_service.send_message(send_message_spec)

    return {
        "data": res,
        "message": "succeed"
    }


@user_router.get("/chat/unread", tags=["User"])
async def get_unread_chat(username: str, role: UserType):
    res = user_service.get_unread_chat(GetUnreadChatSpec(
        username=username,
        role=role,
    ))

    return {
        "data": res,
        "message": "succeed"
    }


@user_router.get("/tes", tags=["User"])
async def get_router():
    confg = ConfigurationService()

    return {
        "data": confg.get_dsn()
    }