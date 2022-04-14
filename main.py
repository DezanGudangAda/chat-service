from fastapi import FastAPI
from injector import Injector
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from gada_chat_service.chat_service.channel.modules import ChannelModule
from gada_chat_service.chat_service.getstream.modules import GetStreamModule
from gada_chat_service.chat_service.migrations.modules import ConnectionModule
from gada_chat_service.chat_service.user.modules import UserModule
from gada_chat_service.core.channel.services.channel_service import ChannelService
from gada_chat_service.core.channel.specs import CreateChannelSpec, GetChannelSpec
from gada_chat_service.core.user.services.user_services import UserService
from gada_chat_service.core.user.specs import GetUserTokenSpec, SendChatSpec

app = FastAPI()

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.post("/user/token", tags=["User"])
async def generate_token(spec: GetUserTokenSpec):
    res = user_service.get_or_create_user_and_token(spec)

    return {
        "data": res,
        "message": "succeed",
    }


# channel
@app.post("/channel", tags=["Channel"])
async def create_channel(spec: CreateChannelSpec):
    res = channel_service.get_or_create_channel(spec)

    return {
        "data": res,
        "message": "succeed"
    }


@app.get("/channel", tags=["Channel"])
async def get_channel(getstream_id: str, target_username: str):
    res = channel_service.get_channel(GetChannelSpec(
        getstream_id=getstream_id,
        target_username=target_username,
    ))

    return {
        "data": res,
        "message": "succeed"
    }


@app.post("/user/chat", tags=["User"])
async def send_message(spec: SendChatSpec):
    res = user_service.send_message(spec)

    return {
        "data": res,
        "message": "succeed"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8300)
