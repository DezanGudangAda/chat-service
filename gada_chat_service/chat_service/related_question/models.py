from sqlalchemy import Column, Integer, String, Boolean

from gada_chat_service.chat_service.base.models import Base


class RelatedQuestion(Base):
    __tablename__ = "related_question"
    id = Column(Integer, autoincrement=True, primary_key=True)
    id_related_answer = Column(Integer)

    question = Column(String)
    is_automate_reply = Column(Boolean)
