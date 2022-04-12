from typing import Optional

from stream_chat import StreamChat
from stream_chat.channel import Channel

from gada_chat_service.core.commons.utils import DictionaryUtil
from gada_chat_service.core.getstream.specs import GenerateUserTokenSpec, GenerateUserTokenResult, CreateChannelSpec, \
    CreateChannelResult, ChatSpec


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
                          custom_data=dict(members=[spec.seller_getstream_id, spec.buyer_getstream_id],
                                           created_by_id="4645"))
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
        meta = {
            "sender": spec.chat_meta.sender,
            "getstream_id": spec.chat_meta.getstream_id,
            "need_reply": spec.chat_meta.need_reply,
            "channel_id": spec.chat_meta.channel_id,
        }

        if spec.chat_meta.reply_option is not None:
            meta["reply_option"] = DictionaryUtil.transform_into_jsonable_array(spec.chat_meta.reply_option),

        data = {
            "product_attachment": DictionaryUtil.transform_into_jsonable_array(spec.product_attachment),
            "chat_meta": meta,
            "order_attachment": spec.order_attachment
        }

        return data

    def send_message(self, spec: ChatSpec):
        chat = self.stream.channel("messaging", spec.chat_meta.channel_id)

        message = self._generate_message(spec)
        return chat.send_message(message, spec.chat_meta.getstream_id)
