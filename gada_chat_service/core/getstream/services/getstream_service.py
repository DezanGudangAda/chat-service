import json
from typing import Optional, List

from stream_chat import StreamChat
from stream_chat.channel import Channel

from gada_chat_service.core.commons.utils import DictionaryUtil
from gada_chat_service.core.getstream.constant import ContextType
from gada_chat_service.core.getstream.specs import GenerateUserTokenSpec, GenerateUserTokenResult, CreateChannelSpec, \
    CreateChannelResult, ChatSpec, ChatExternalDataSpec, ProductAttachmentSpec, OrderAttachmentSpec, ChatMetaSpec


class GetStreamService:
    def __init__(self):
        self.stream = StreamChat(api_key="edn3c63hd6cp",
                                 api_secret="nkgvbjazag5na7watg3jcfnhhdvsufud2zg468743grkmpexqd54cjbykdspzvwd")

    def generate_token(self, spec: GenerateUserTokenSpec) -> Optional[GenerateUserTokenResult]:
        stream_id = spec.username + "_" + spec.type.value.lower()

        token = self.stream.create_token(stream_id)
        self.stream.upsert_user({"id": stream_id})

        return GenerateUserTokenResult(
            token=token,
            stream_id=stream_id
        )

    def create_channel(self, spec: CreateChannelSpec) -> Optional[CreateChannelResult]:
        channel = Channel(self.stream, "messaging", None,
                          custom_data=dict(members=[spec.seller_getstream_id, spec.buyer_getstream_id], created_by_id="4645"))
        channel.query()

        return CreateChannelResult(
            channel_id=channel.id,
            channel_name=channel.id,
            seller_getstream_id=spec.seller_getstream_id,
            buyer_getstream_id=spec.buyer_getstream_id
        )

    def _generate_message(self, spec: ChatSpec) -> dict:
        message = {"text": spec.message, "external_data": self._external_data_to_json(spec)}

        return message

    def _external_data_to_json(self, spec: ChatSpec) -> dict:
        data = {
            "product_attachment": DictionaryUtil.transform_into_jsonable_array(spec.product_attachment),
            "chat_meta": spec.chat_meta,
            "order_attachment": spec.order_attachment
        }

        return data

    def send_message(self, spec: ChatSpec):
        chat = self.stream.channel("messaging", spec.chat_meta.channel_id)

        message = self._generate_message(spec)
        return chat.send_message(message, spec.chat_meta.channel_id)
