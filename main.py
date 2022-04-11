from fastapi import FastAPI

from gada_chat_service.core.getstream.constant import UserType
from gada_chat_service.core.getstream.services.getstream_service import GetStreamService
from gada_chat_service.core.getstream.specs import GenerateUserTokenSpec, CreateChannelSpec, ChatSpec

app = FastAPI()

service = GetStreamService()


@app.post("/user/token")
async def generate_token(username: str, user_type: UserType):
    res = service.generate_token(GenerateUserTokenSpec(
        username=username,
        type=user_type
    ))

    return {
        "message": res
    }


@app.post("/channel")
async def create_channel(seller_id: str, buyer_id: str):
    res = service.create_channel(CreateChannelSpec(
        buyer_id=buyer_id,
        seller_id=seller_id
    ))

    return {
        "message": res
    }


@app.post("/message")
async def send_message(chat: ChatSpec):
    res = service.send_message(chat)

    return {
        "message": res
    }
