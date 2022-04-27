from sqlalchemy import Column, Integer, String

from gada_chat_service.chat_service.base.models import Base
from gada_chat_service.core.commons.utils import ObjectMapperUtil
from gada_chat_service.core.related_answer.models import RelatedAnswerDomain


class RelatedAnswer(Base):
    __tablename__ = "related_answer"
    id = Column(Integer, autoincrement=True, primary_key=True)

    answer = Column(String)
    trigger_action = Column(String)
    code = Column(String)

    def to_domain(self) -> RelatedAnswerDomain:
        domain = ObjectMapperUtil.map(self, RelatedAnswerDomain)
        return domain
