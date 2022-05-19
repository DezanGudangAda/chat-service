from fastapi import APIRouter

from gada_chat_service.chat_service.injector import injector
from gada_chat_service.core.getstream.constant import UserType
from gada_chat_service.core.user.services.user_services import UserService
from gada_chat_service.core.user.specs import GetUserTokenSpec, SendChatSpec, GetUnreadChatSpec

user_service: UserService = injector.get(
    UserService
)

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@user_router.post("/token", tags=["User"])
async def generate_token(spec: GetUserTokenSpec):
    res = user_service.get_or_create_user_and_token(spec)

    return {
        "data": res,
        "message": "succeed",
    }


@user_router.post("/chat", tags=["User"])
async def send_message(spec: SendChatSpec):
    res = user_service.send_message(spec)

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