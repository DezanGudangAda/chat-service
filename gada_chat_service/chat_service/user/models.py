from sqlalchemy import Column, Integer, String

from gada_chat_service.chat_service.base.models import Base
from gada_chat_service.core.commons.utils import ObjectMapperUtil
from gada_chat_service.core.user.models import UserDomain


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String)
    stream_token = Column(String)
    account_type = Column(String, nullable=False)
    getstream_id = Column(String)
    name = Column(String)

    def to_domain(self) -> UserDomain:
        domain = ObjectMapperUtil.map(self, UserDomain)
        return domain
