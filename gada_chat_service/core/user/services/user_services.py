from typing import Optional

from fastapi import HTTPException
from injector import inject

from gada_chat_service.core.channel.constants import OrderType, SELLER_INDEX, BUYER_INDEX
# from gada_chat_service.core.channel.services.channel_service import ChannelService
from gada_chat_service.core.channel.specs import GetChannelListSpec
from gada_chat_service.core.qna_journey.services.qna_journey_service import QnaJourneyService
from gada_chat_service.core.qna_journey.specs import GetNextNodesSpec
from gada_chat_service.core.user.ports import IUserServiceProvider
from gada_chat_service.core.channel.accessors.channel_accessor import IChannelAccessor
from gada_chat_service.core.getstream.constant import ContextType, UserType
from gada_chat_service.core.getstream.services.getstream_service import GetStreamService
from gada_chat_service.core.getstream.specs import GenerateUserTokenSpec, ChatSpec, ProductAttachmentSpec, \
    OrderAttachmentSpec, ChatMetaSpec, ReplyOptionSpec
from gada_chat_service.core.user.accessor.user_accessor import IUserAccessor
from gada_chat_service.core.user.models import UserDomain
from gada_chat_service.core.user.specs import InsertUserTokenSpec, SendChatSpec, RegisterUserSpec, GetUnreadChatSpec, \
    GetUnreadChatReturn, GetUserTokenSpec


class UserService:
    @inject
    def __init__(
            self,
            stream_service: GetStreamService,
            user_accessor: IUserAccessor,
            channel_accessor: IChannelAccessor,
            user_service_provider: IUserServiceProvider,
            qna_journey_service: QnaJourneyService
    ):
        self.qna_journey_service = qna_journey_service
        self.user_service_provider = user_service_provider
        self.channel_accessor = channel_accessor
        self.stream_service = stream_service
        self.user_accessor = user_accessor

    def register_user(self, spec: RegisterUserSpec) -> Optional[UserDomain]:
        stream_token = self.stream_service.generate_token(GenerateUserTokenSpec(
            username=spec.identity,
            type=spec.user_type
        ))

        new_token = self.user_accessor.create_user_and_token(InsertUserTokenSpec(
            username=spec.identity,
            type=spec.user_type,
            token=stream_token.token,
            getstream_id=stream_token.stream_id,
            name=spec.name
        ))

        return new_token

    def get_user_detail(self, identity: str, user_type: UserType) -> Optional[UserDomain]:
        is_seller = True
        if user_type == UserType.BUYER:
            is_seller = False

        current_user = self.user_accessor.get_user_detail(identity, is_seller)
        if current_user is not None:
            return current_user

        get_from_api = self.user_service_provider.get_user_marketplace_detail(identity, is_seller)
        if get_from_api is None:
            return None

        return self.register_user(
            RegisterUserSpec(
                user_type=user_type,
                identity=identity,
                name=get_from_api.name
            )
        )

    def send_message(self, spec: SendChatSpec):
        channel = self.channel_accessor.get_channel_by_id(spec.channel_id)
        if channel is None:
            raise HTTPException(status_code=400, detail="channel not found")

        user = self.get_user_detail(spec.identity, spec.role)
        if user is None:
            raise HTTPException(status_code=400, detail="user is not valid")

        product_attachments = []
        order_attachments = None
        # validate current path

        current_node = self.qna_journey_service.get_node_detail(spec.message_code)

        current_path = ""
        if spec.current_path == "":
            current_path = f"{spec.message_code}"
        else:
            current_path = f"{spec.current_path}/{spec.message_code}"

        next_path = self.qna_journey_service.get_next_nodes(GetNextNodesSpec(
            current_path=current_path
        ))

        # get product attachment
        if spec.context is not None:
            if spec.context.type == ContextType.PRODUCT:
                for ids in spec.context.related_id:
                    product = ProductAttachmentSpec(
                        image_url="https://marketplace-static.gudangada.com/email-assets/logo.png",
                        is_available=True,
                        current_stock=100,
                        price="Rp 25,000",
                        name="Product #" + str(ids),
                        id=ids
                    )

                    product_attachments.append(product)

            # get order attachment
            if spec.context.type == ContextType.ORDER:
                if len(spec.context.related_id) != 1:
                    raise HTTPException(detail="context order only can contain 1 order code", status_code=400)

                order_attachments = OrderAttachmentSpec(
                    image_url="https://marketplace-static.gudangada.com/email-assets/logo.png",
                    price="Rp 25,000",
                    order_code="ORDER-" + str(spec.context.related_id[0]),
                    status="PENDING"
                )

        reply_option = []
        for node in next_path.nodes:
            reply_option.append(ReplyOptionSpec(
                message=node.text,
                message_code=node.code
            ))

        # get chat meta
        chat_meta = ChatMetaSpec(
            sender=user.username,
            getstream_id=user.getstream_id,
            need_reply=True,
            reply_option=reply_option,
            channel_id=channel.id,
            current_path=current_path
        )

        chat_spec = ChatSpec(
            message=current_node.text,
            chat_meta=chat_meta,
            order_attachment=order_attachments,
            product_attachment=product_attachments
        )

        chat = self.stream_service.send_message(chat_spec)
        return chat

    def get_unread_chat(self, spec: GetUnreadChatSpec) -> Optional[GetUnreadChatReturn]:
        is_valid = True
        is_seller = True
        index = SELLER_INDEX

        if spec.role == UserType.BUYER:
            is_seller = False
            index = BUYER_INDEX

        current_user = self.user_accessor.get_user_by_username_and_type(GetUserTokenSpec(
            username=spec.username,
            type=spec.role
        ))

        if current_user is None:
            is_valid = False

        get_from_api = self.user_service_provider.get_user_marketplace_detail(spec.username, is_seller)

        if get_from_api is None and not is_valid:
            raise HTTPException(status_code=400, detail="user not valid")

        register_user = self.register_user(RegisterUserSpec(
            identity=spec.username,
            name=get_from_api.name,
            user_type=spec.role,
        ))

        if not is_valid and get_from_api is not None:
            return GetUnreadChatReturn(
                unread_chat="0"
            )

        detail_stream_channel = self.stream_service.get_channel_detail(current_user.getstream_id)

        get_channels = detail_stream_channel.get("channels")
        total = 0
        for chan in get_channels:
            messages = chan.get("messages")
            if not messages:
                continue

            read = chan.get("read")
            if len(read) != 2:
                continue

            total += int(read[index].get("unread_messages"))

        return GetUnreadChatReturn(
            unread_chat=str(total)
        )
