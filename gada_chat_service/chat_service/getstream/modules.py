from injector import Binder, Module, singleton

from gada_chat_service.core.getstream.services.getstream_service import GetStreamService


class GetStreamModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            GetStreamService,
            to=GetStreamService,
            scope=singleton,
        )
