import json
from typing import Optional

from stream_chat import StreamChat
from stream_chat.channel import Channel

from gada_chat_service.core.commons.utils import DictionaryUtil
from gada_chat_service.core.config.services.configuration_service import ConfigurationService
from gada_chat_service.core.getstream.specs import GenerateUserTokenSpec, GenerateUserTokenResult, CreateChannelSpec, \
    CreateChannelResult, ChatSpec, ChannelDetail


class GetStreamService:
    def __init__(self):
        self.configuration_service = ConfigurationService()
        self.stream = StreamChat(api_key=self.configuration_service.get_config().get_stream.api_key,
                                 api_secret=self.configuration_service.get_config().get_stream.secret)

    def generate_token(self, spec: GenerateUserTokenSpec) -> Optional[GenerateUserTokenResult]:
        stream_id = spec.username + "_" + spec.type.value.lower()

        token = self.stream.create_token(stream_id)
        self.stream.upsert_user({"id": stream_id})

        return GenerateUserTokenResult(
            token=token,
            stream_id=stream_id
        )

    def create_channel(self, spec: CreateChannelSpec) -> Optional[CreateChannelResult]:
        # TODO: Config created by id
        channel = Channel(self.stream, "messaging", None,
                          custom_data=dict(members=[spec.seller_getstream_id, spec.buyer_getstream_id],
                                           created_by_id="4645",
                                           seller_name=spec.seller_name,
                                           buyer_name=spec.buyer_name))
        data = channel.query()

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
            "current_path": spec.chat_meta.current_path
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

    def get_channel_detail(self, getstream_id: str):
        data = self.stream.query_channels(
            {
                "members": {
                    "$in": [getstream_id]
                }
            },
            message_limit=1,
        )
        return data

    def deep_search_message_in_channel(self, getstream_id: str, keyword):
        filters = {
            "members": {
                "$in": [getstream_id]
            }
        }

        result = self.stream.search(
            filters,
            keyword,
            limit=100
        )

        return result.get("results")

    def get_channel(self, channel_id: str):
        filters = {
            "cid": {
                "$eq": channel_id
            }
        }

        result = self.stream.query_channels(filters, message_limit=1)
        return result.get("channels")

    def query_channel_based_sender_name(self, sender_name: str):
        filters = {
            "seller_name": {
                "autocomplete": sender_name
            }
        }

        result = self.stream.query_channels(filters, message_limit=1)

        return result