from sqlalchemy import Column, Integer, String

from gada_chat_service.chat_service.base.models import Base


class QnaJourney(Base):
    __tablename__ = "qna_journey"
    id = Column(Integer, autoincrement=True, primary_key=True)

    path = Column(String)
