from fastapi import APIRouter

from gada_chat_service.chat_service.injector import injector
from gada_chat_service.core.channel.services.channel_service import ChannelService
from gada_chat_service.core.channel.specs import CreateChannelSpec, GetChannelSpec

channel_service: ChannelService = injector.get(
    ChannelService
)

channel_router = APIRouter(
    prefix="/channel",
    tags=["Channel"],
)


@channel_router.post("", tags=["Channel"])
async def create_channel(spec: CreateChannelSpec):
    res = channel_service.get_or_create_channel(spec)

    return {
        "data": res,
        "message": "succeed"
    }


@channel_router.get("", tags=["Channel"])
async def get_channel(getstream_id: str, target_username: str):
    res = channel_service.get_channel(GetChannelSpec(
        getstream_id=getstream_id,
        target_username=target_username,
    ))

    return {
        "data": res,
        "message": "succeed"
    }
