from fastapi import FastAPI
from injector import Injector

from gada_chat_service.chat_service.channel.modules import ChannelModule
from gada_chat_service.chat_service.getstream.modules import GetStreamModule
from gada_chat_service.chat_service.migrations.modules import ConnectionModule
from gada_chat_service.chat_service.user.modules import UserModule
from gada_chat_service.core.channel.services.channel_service import ChannelService
from gada_chat_service.core.channel.specs import GetChannelByUsersSpec
from gada_chat_service.core.user.services.user_services import UserService
from gada_chat_service.core.user.specs import GetUserTokenSpec, SendChatSpec

app = FastAPI()

injector = Injector(
    [
        UserModule,
        GetStreamModule,
        ConnectionModule,
        ChannelModule,
    ]
)

user_service: UserService = injector.get(
    UserService
)

channel_service: ChannelService = injector.get(
    ChannelService
)


@app.post("/user/token")
async def generate_token(spec: GetUserTokenSpec):
    res = user_service.get_or_create_user_and_token(spec)

    return {
        "data": res,
        "message": "succeed",
    }


# channel
@app.post("/channel")
async def get_or_create_channel(spec: GetChannelByUsersSpec):
    res = channel_service.get_or_create_channel(spec)

    return {
        "data": res,
        "message": "succeed"
    }


@app.post("/user/chat")
async def send_message(spec: SendChatSpec):
    res = user_service.send_message(spec)

    return {
        "data": res,
        "message": "succeed"
    }
