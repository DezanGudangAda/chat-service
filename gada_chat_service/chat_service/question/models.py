from sqlalchemy import Column, Integer, String, Boolean

from gada_chat_service.chat_service.base.models import Base


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    is_automate_reply = Column(Boolean)
