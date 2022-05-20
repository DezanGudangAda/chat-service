import json
import os

from gada_chat_service.core.config.models import Configuration
from gada_chat_service.core.config.utils import EnhancedJSONEncoder, EmployeeEncoder
from dacite import from_dict


class ConfigurationService:
    def __init__(self):
        ROOT_DIR = os.path.abspath(os.curdir)
        open_json = open(ROOT_DIR + "/config.json")
        load_json = json.load(open_json)
        self.config = from_dict(data_class=Configuration, data=load_json)

    def get_config(self) -> Configuration:
        return self.config

    def get_dsn(self) -> str:
        return f"postgresql+psycopg2://{self.config.database.username}:" \
               f"{self.config.database.password}@{self.config.database.host}/{self.config.database.db}"
