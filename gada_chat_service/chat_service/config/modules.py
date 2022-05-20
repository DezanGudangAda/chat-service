from injector import Binder, Module, singleton

from gada_chat_service.core.config.services.configuration_service import ConfigurationService


class ConfigurationModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            ConfigurationService,
            to=ConfigurationService,
            scope=singleton,
        )
