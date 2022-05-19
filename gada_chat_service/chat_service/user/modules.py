from injector import Binder, Module, singleton

from gada_chat_service.chat_service.user.accessors.user_accessor import UserAccessor
from gada_chat_service.chat_service.user.adapters import UserServiceProvider
from gada_chat_service.core.user.accessor.user_accessor import IUserAccessor
from gada_chat_service.core.user.ports import IUserServiceProvider
from gada_chat_service.core.user.services.user_services import UserService


class UserModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            IUserAccessor,
            to=UserAccessor,
            scope=singleton,
        )
        binder.bind(
            UserService,
            to=UserService,
            scope=singleton,
        )
        binder.bind(
            IUserServiceProvider,
            to=UserServiceProvider,
            scope=singleton,
        )