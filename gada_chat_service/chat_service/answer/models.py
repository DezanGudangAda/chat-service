from sqlalchemy import Column, Integer, String

from gada_chat_service.chat_service.base.models import Base


class Answer(Base):
    __tablename__ = "answer"
    id = Column(Integer, autoincrement=True, primary_key=True)

    answer = Column(String)
    question_id = Column(Integer)