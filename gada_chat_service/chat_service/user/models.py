from sqlalchemy import Column, Integer, String

from gada_chat_service.chat_service.base.models import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String)
    stream_token = Column(String)
    account_type = Column(String, nullable=False)
