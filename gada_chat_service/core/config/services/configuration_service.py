import json
import os

from gada_chat_service.core.config.models import Configuration
from gada_chat_service.core.config.utils import EnhancedJSONEncoder, EmployeeEncoder
from dacite import from_dict


class ConfigurationService:
    def __init__(self):
        path = "../../config.json"
        if os.getenv("env") != "MIGRATION":
            ROOT_DIR = os.path.abspath(os.curdir)
            path = ROOT_DIR + "/config.json"

        open_json = open(path)
        load_json = json.load(open_json)
        self.config = from_dict(data_class=Configuration, data=load_json)

    def get_config(self) -> Configuration:
        return self.config

    def get_dsn(self) -> str:
        return f"postgresql+psycopg2://{self.config.database.username}:" \
               f"{self.config.database.password}@{self.config.database.host}:{self.config.database.port}" \
               f"/{self.config.database.db}"

    @staticmethod
    def get_env_dsn() -> str:
        if os.getenv("env") != "MIGRATION":
            config = ConfigurationService()
            return config.get_dsn()

        db_host = os.getenv("DB_HOST")
        db_username = os.getenv("DB_USERNAME")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        db_port = os.getenv("DB_PORT")

        return f"postgresql+psycopg2://{db_username}:" \
               f"{db_password}@{db_host}:{db_port}" \
               f"/{db_name}"
