from injector import Binder, Module, singleton
from sqlalchemy.orm import Session

from gada_chat_service.chat_service.migrations.connection import gas
from gada_chat_service.core.getstream.services.getstream_service import GetStreamService


class ConnectionModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            Session,
            to=gas,
            scope=singleton,
        )
