from sqlalchemy import Column, Integer, String

from gada_chat_service.chat_service.base.models import Base
from gada_chat_service.chat_service.user.constant import UserType


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String, unique=True)
    stream_token = Column(String)
    account_type = Column(String, nullable=False)
