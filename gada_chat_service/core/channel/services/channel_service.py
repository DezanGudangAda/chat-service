import json
from typing import Optional

from fastapi import HTTPException
from injector import inject

from gada_chat_service.chat_service.user.accessors.user_accessor import UserAccessor
from gada_chat_service.core.channel.accessors.channel_accessor import IChannelAccessor
from gada_chat_service.core.channel.constants import TargetType, SELLER_INDEX, BUYER_INDEX, SELLER_NAME_STREAM_KEY, \
    BUYER_NAME_STREAM_KEY
from gada_chat_service.core.channel.models import ChannelDomain
from gada_chat_service.core.channel.specs import GetChannelListSpec, \
    GetChannelListReturn, ChannelRoomReturn, SearchChannelSpec, SearchChannelReturn
from gada_chat_service.core.channel.specs import InsertChannelSpec, GetChannelSpec, GetChannelDbSpec
from gada_chat_service.core.getstream.constant import UserType
from gada_chat_service.core.getstream.services.getstream_service import GetStreamService
from gada_chat_service.core.getstream.specs import CreateChannelSpec as CreateStreamChannel
from gada_chat_service.core.user.services.user_services import UserService


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

    def create_channel(self, spec: InsertChannelSpec) -> Optional[ChannelDomain]:
        create_channel = self.stream_service.create_channel(CreateStreamChannel(
            seller_getstream_id=spec.seller_getstream_id,
            buyer_getstream_id=spec.buyer_getstream_id,
            seller_name=spec.seller_name,
            buyer_name=spec.buyer_name
        ))

        new_channel = self.channel_accessor.create_channel(InsertChannelSpec(
            channel_id=create_channel.channel_id,
            channel_name=spec.channel_name,
            seller_getstream_id=spec.seller_getstream_id,
            buyer_getstream_id=spec.buyer_getstream_id,
            buyer_name=spec.buyer_name,
            seller_name=spec.seller_name
        ))

        return new_channel

    def open_channel(self, spec: GetChannelSpec) -> Optional[ChannelDomain]:
        seller_identity = None
        buyer_identity = None

        if spec.target_type.SELLER == TargetType.SELLER:
            seller_identity = spec.target
            buyer_identity = spec.username
        elif spec.target_type.BUYER == TargetType.BUYER:
            seller_identity = spec.username
            buyer_identity = spec.target

        seller_chat_account = self.user_service.get_user_detail(seller_identity, UserType.SELLER)
        if seller_chat_account is None:
            raise HTTPException(status_code=400, detail="seller not valid")

        buyer_chat_account = self.user_service.get_user_detail(buyer_identity, UserType.BUYER)
        if buyer_chat_account is None:
            raise HTTPException(status_code=400, detail="buyer not valid")

        current_channel = self.channel_accessor.get_channel_by_users(GetChannelDbSpec(
            seller_getstream_id=seller_chat_account.getstream_id,
            buyer_getstream_id=buyer_chat_account.getstream_id
        ))

        if current_channel is not None:
            return current_channel

        stream_channel = self.stream_service.create_channel(CreateStreamChannel(
            seller_getstream_id=seller_chat_account.getstream_id,
            buyer_getstream_id=buyer_chat_account.getstream_id,
            seller_name=seller_chat_account.name,
            buyer_name=buyer_chat_account.name
        ))

        return self.create_channel(InsertChannelSpec(
            seller_getstream_id=seller_chat_account.getstream_id,
            buyer_getstream_id=buyer_chat_account.getstream_id,
            channel_id=stream_channel.channel_id,
            channel_name=stream_channel.channel_name,
            seller_name=seller_chat_account.name,
            buyer_name=buyer_chat_account.name
        ))

    def channel_list(self, spec: GetChannelListSpec) -> Optional[GetChannelListReturn]:
        index = SELLER_INDEX
        key_name = SELLER_NAME_STREAM_KEY
        if spec.role == UserType.BUYER:
            index = BUYER_INDEX
            key_name = BUYER_NAME_STREAM_KEY

        user = self.user_service.get_user_detail(spec.identity, spec.role)
        if user is None:
            raise HTTPException(status_code=400, detail="user not valid")

        detail_stream_channel = self.stream_service.get_channel_detail(user.getstream_id)
        result = []

        get_channels = detail_stream_channel.get("channels")
        for chan in get_channels:
            messages = chan.get("messages")
            if not messages:
                continue

            read = chan.get("read")
            if len(read) != 2:
                continue

            channel_detail = chan.get("channel")

            unread_message = read[index].get("unread_messages")
            last_message_at = messages[0].get("created_at")
            last_message = messages[0].get("text")
            channel_id = channel_detail.get("id")
            sender = channel_detail.get(key_name)
            if sender is None:
                sender = "No Name"

            result.append(ChannelRoomReturn(
                channel_id=channel_id,
                name=sender,
                last_chat=last_message,
                unread_chat=unread_message,
                date=last_message_at
            ))

        return GetChannelListReturn(
            chat_rooms=result,
        )

    def search_channel(self, spec: SearchChannelSpec) -> Optional[SearchChannelReturn]:
        role = UserType.BUYER
        index = BUYER_INDEX
        key_name = BUYER_NAME_STREAM_KEY

        if role == UserType.SELLER:
            role = UserType.SELLER
            index = SELLER_INDEX
            key_name = SELLER_NAME_STREAM_KEY

        user = self.user_service.get_user_detail(spec.identity, role)
        if user is None:
            raise HTTPException(status_code=400, detail="user not valid")

        channels = self.stream_service.deep_search_message_in_channel(user.getstream_id, spec.keyword)

        in_message = []
        previous_channel_id = ""
        for channel in channels:
            message = channel["message"]
            channel_data = message["channel"]
            channel_cid = channel_data["cid"]

            if previous_channel_id == "":
                previous_channel_id = channel_cid
            elif previous_channel_id == channel_cid:
                continue

            get_channel_detail = self.stream_service.get_channel(channel_id=channel_cid)[0]

            read = get_channel_detail.get("read")
            messages = get_channel_detail.get("messages")

            unread_message = read[index].get("unread_messages")
            last_message_at = messages[0].get("created_at")
            last_message = messages[0].get("text")
            channel_id = channel_data.get("id")
            sender = get_channel_detail.get("channel").get(key_name)
            if sender is None:
                sender = "No Name"

            in_message.append(ChannelRoomReturn(
                channel_id=channel_id,
                name=sender,
                last_chat=last_message,
                unread_chat=unread_message,
                date=last_message_at
            ))

        return SearchChannelReturn(
            in_chat=in_message,
            sender=[]
        )
