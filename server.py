import sentry_sdk

from gada_chat_service.core.config.services.configuration_service import ConfigurationService


def init_web_server():
    get_config_setting = ConfigurationService()
    print(get_config_setting.config.sentry_dsn)
    sentry_sdk.init(
        get_config_setting.config.sentry_dsn,
        traces_sample_rate=1.0,
        send_default_pii=True
    )


