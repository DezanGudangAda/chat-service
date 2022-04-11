from typing import Optional

from injector import inject

from gada_chat_service.core.channel.accessors.channel_accessor import IChannelAccessor
from gada_chat_service.core.channel.models import ChannelDomain
from gada_chat_service.core.channel.specs import InsertChannelSpec, GetChannelByUsersSpec
from gada_chat_service.core.getstream.services.getstream_service import GetStreamService
from gada_chat_service.core.getstream.specs import CreateChannelSpec


class ChannelService:
    @inject
    def __init__(
            self,
            channel_accessor: IChannelAccessor,
            stream_service: GetStreamService,
    ):
        self.channel_accessor = channel_accessor
        self.stream_service = stream_service

    def get_or_create_channel(self, spec: GetChannelByUsersSpec) -> Optional[ChannelDomain]:
        channel = self.channel_accessor.get_channel_by_users(spec)
        if channel is not None:
            return channel

        create_channel = self.stream_service.create_channel(CreateChannelSpec(
            seller_username=spec.seller_username,
            buyer_username=spec.buyer_username,
        ))

        new_channel = self.channel_accessor.create_channel(InsertChannelSpec(
            channel_id=create_channel.channel_id,
            channel_name=f"{spec.seller_username}{spec.buyer_username}",
            seller_username=spec.seller_username,
            buyer_username=spec.buyer_username,
        ))

        return new_channel
