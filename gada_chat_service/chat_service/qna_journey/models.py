from sqlalchemy import Column, Integer, String

from gada_chat_service.chat_service.base.models import Base
from gada_chat_service.core.commons.utils import ObjectMapperUtil
from gada_chat_service.core.qna_journey.models import QnaJourneyDomain


class QnaJourney(Base):
    __tablename__ = "qna_journey"
    id = Column(Integer, autoincrement=True, primary_key=True)

    path = Column(String)

    def to_domain(self) -> QnaJourneyDomain:
        domain = ObjectMapperUtil.map(self, QnaJourneyDomain)
        return domain
