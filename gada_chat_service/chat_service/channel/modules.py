from injector import Binder, Module, singleton

from gada_chat_service.chat_service.channel.accessor.channel_accessor import ChannelAccessor
from gada_chat_service.core.channel.accessors.channel_accessor import IChannelAccessor
from gada_chat_service.core.channel.services.channel_service import ChannelService


class ChannelModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            IChannelAccessor,
            to=ChannelAccessor,
            scope=singleton,
        )
        binder.bind(
            ChannelService,
            to=ChannelService,
            scope=singleton,
        )