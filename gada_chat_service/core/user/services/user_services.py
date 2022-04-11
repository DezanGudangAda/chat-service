from typing import Optional

from injector import inject

from gada_chat_service.core.channel.accessors.channel_accessor import IChannelAccessor
from gada_chat_service.core.getstream.constant import ContextType
from gada_chat_service.core.getstream.services.getstream_service import GetStreamService
from gada_chat_service.core.getstream.specs import GenerateUserTokenSpec, ChatSpec, ProductAttachmentSpec, \
    OrderAttachmentSpec, ChatMetaSpec
from gada_chat_service.core.user.accessor.user_accessor import IUserAccessor
from gada_chat_service.core.user.models import UserDomain
from gada_chat_service.core.user.specs import GetUserTokenSpec, InsertUserTokenSpec, SendChatSpec


class UserService:
    @inject
    def __init__(
            self,
            stream_service: GetStreamService,
            user_accessor: IUserAccessor,
            channel_accessor: IChannelAccessor,
    ):
        self.channel_accessor = channel_accessor
        self.stream_service = stream_service
        self.user_accessor = user_accessor

    def get_or_create_user_and_token(self, spec: GetUserTokenSpec) -> Optional[UserDomain]:
        existing_user = self.user_accessor.get_user_by_username_and_type(spec)
        if existing_user is not None:
            return existing_user

        stream_token = self.stream_service.generate_token(GenerateUserTokenSpec(
            username=spec.username,
            type=spec.type
        ))

        new_token = self.user_accessor.create_user_and_token(InsertUserTokenSpec(
            username=spec.username,
            type=spec.type,
            token=stream_token.token,
            getstream_id=stream_token.stream_id
        ))

        return new_token

    def send_message(self, spec: SendChatSpec):
        channel = self.channel_accessor.get_channel_by_id(spec.channel_id)
        if channel is None:
            raise Exception("channel not found")

        user = self.user_accessor.get_user_by_getstream_id(spec.getstream_id)
        if user is None:
            raise Exception("user is not registered")

        product_attachments = []
        order_attachments = None
        chat_meta = None

        # get product attachment
        if spec.context.type == ContextType.PRODUCT:
            for ids in spec.context.related_id:
                product = ProductAttachmentSpec(
                    image_url="https://marketplace-static.gudangada.com/email-assets/logo.png",
                    is_available=True,
                    current_stock=100,
                    price="Rp 25,000",
                    name="Product #" + str(ids)
                )

                product_attachments.append(product)

        # get order attachment
        if spec.context.type == ContextType.ORDER:
            if len(spec.context.related_id) != 1:
                raise Exception("context order only can contain 1 order code")

            order_attachments = OrderAttachmentSpec(
                image_url="https://marketplace-static.gudangada.com/email-assets/logo.png",
                price="Rp 25,000",
                order_code="ORDER-" + str(spec.context.related_id[0]),
                status="PENDING"
            )

        # get chat meta
        chat_meta = ChatMetaSpec(
            sender=user.username,
            getstream_id=user.getstream_id,
            need_reply=False,
            reply_option=None,
            channel_id=channel.id,
        )

        chat_spec = ChatSpec(
            message=spec.message,
            chat_meta=chat_meta,
            order_attachment=order_attachments,
            product_attachment=product_attachments
        )

        chat = self.stream_service.send_message(chat_spec)
        return chat
