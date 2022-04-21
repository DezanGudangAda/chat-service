from typing import Optional

from fastapi import HTTPException
from injector import inject

from gada_chat_service.chat_service.user.accessors.user_accessor import UserAccessor
from gada_chat_service.core.channel.accessors.channel_accessor import IChannelAccessor
from gada_chat_service.core.channel.models import ChannelDomain
from gada_chat_service.core.channel.specs import InsertChannelSpec, CreateChannelSpec, GetChannelSpec, GetChannelDbSpec
from gada_chat_service.core.getstream.constant import UserType
from gada_chat_service.core.getstream.services.getstream_service import GetStreamService
from gada_chat_service.core.getstream.specs import CreateChannelSpec
from gada_chat_service.core.channel.specs import CreateChannelSpec as CreateChanSpec
from gada_chat_service.core.user.services.user_services import UserService
from gada_chat_service.core.user.specs import GetUserTokenSpec


class ChannelService:
    @inject
    def __init__(
            self,
            channel_accessor: IChannelAccessor,
            stream_service: GetStreamService,
            user_accessor: UserAccessor,
            user_service: UserService,
    ):
        self.user_service = user_service
        self.user_accessor = user_accessor
        self.channel_accessor = channel_accessor
        self.stream_service = stream_service

    def get_or_create_channel(self, spec: CreateChanSpec) -> Optional[ChannelDomain]:
        seller_stream_account = self.user_service.get_or_create_user_and_token(GetUserTokenSpec(
            username=spec.seller_username,
            type=UserType.SELLER
        ))

        channel = self.channel_accessor.get_channel_by_users(GetChannelDbSpec(
            seller_getstream_id=seller_stream_account.getstream_id,
            buyer_getstream_id=spec.buyer_getstream_id
        ))
        if channel is not None:
            return channel

        create_channel = self.stream_service.create_channel(CreateChannelSpec(
            seller_getstream_id=seller_stream_account.getstream_id,
            buyer_getstream_id=spec.buyer_getstream_id,
        ))

        new_channel = self.channel_accessor.create_channel(InsertChannelSpec(
            channel_id=create_channel.channel_id,
            channel_name=f"{seller_stream_account.getstream_id}-{spec.buyer_getstream_id}",
            seller_getstream_id=seller_stream_account.getstream_id,
            buyer_getstream_id=spec.buyer_getstream_id,
        ))

        return new_channel

    def get_channel(self, spec: GetChannelSpec) -> Optional[ChannelDomain]:
        check_getstream = self.user_accessor.get_user_by_getstream_id(spec.getstream_id)

        if check_getstream is None:
            raise HTTPException(status_code=404, detail="user not registered")

        if check_getstream.account_type == UserType.SELLER.value:
            target_user = self.user_service.get_or_create_user_and_token(GetUserTokenSpec(
                username=spec.target_username,
                type=UserType.BUYER
            ))

            channel = self.channel_accessor.get_channel_by_users(GetChannelDbSpec(
                buyer_getstream_id=spec.getstream_id,
                seller_getstream_id=target_user.getstream_id
            ))

            if channel is None:
                raise HTTPException(status_code=404, detail="Channel not found")

            return channel

        target_user = self.user_service.get_or_create_user_and_token(GetUserTokenSpec(
            username=spec.target_username,
            type=UserType.SELLER
        ))

        channel = self.channel_accessor.get_channel_by_users(GetChannelDbSpec(
            buyer_getstream_id=check_getstream.getstream_id,
            seller_getstream_id=target_user.getstream_id
        ))

        if channel is None:
            raise HTTPException(status_code=404, detail="Channel not found")

        return channel
