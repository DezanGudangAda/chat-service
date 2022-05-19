from fastapi import APIRouter

from gada_chat_service.chat_service.injector import injector
from gada_chat_service.core.channel.constants import TargetType, OrderType
from gada_chat_service.core.channel.services.channel_service import ChannelService
from gada_chat_service.core.channel.specs import CreateChannelSpec, GetChannelSpec, GetChannelListSpec
from gada_chat_service.core.getstream.constant import UserType

channel_service: ChannelService = injector.get(
    ChannelService
)

channel_router = APIRouter(
    prefix="/channel",
    tags=["Channel"],
)


@channel_router.post("", tags=["Channel"])
async def create_channel(spec: GetChannelSpec):
    res = channel_service.open_channel(spec)

    return {
        "data": res,
        "message": "succeed"
    }

@channel_router.get("/list", tags=["Channel"])
async def get_list_of_channel(role: UserType, order: OrderType, identity: str):
    res = channel_service.channel_list(GetChannelListSpec(
        identity=identity,
        order=order,
        role=role,
    ))

    return {
        "data": res,
        "message": "succeed"
    }
