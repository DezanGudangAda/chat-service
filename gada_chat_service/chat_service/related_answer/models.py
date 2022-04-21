from sqlalchemy import Column, Integer, String

from gada_chat_service.chat_service.base.models import Base


class RelatedAnswer(Base):
    __tablename__ = "related_answer"
    id = Column(Integer, autoincrement=True, primary_key=True)

    answer = Column(String)
    trigger_action = Column(String)
    code = Column(String)

