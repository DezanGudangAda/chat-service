from sqlalchemy import Column, Integer, String, Boolean

from gada_chat_service.chat_service.base.models import Base
from gada_chat_service.core.commons.utils import ObjectMapperUtil
from gada_chat_service.core.related_question.models import RelatedQuestionDomain


class RelatedQuestion(Base):
    __tablename__ = "related_question"
    id = Column(Integer, autoincrement=True, primary_key=True)

    question = Column(String)
    is_automate_reply = Column(Boolean)
    trigger_action = Column(String)
    context = Column(String)
    code = Column(String)

    def to_domain(self) -> RelatedQuestionDomain:
        domain = ObjectMapperUtil.map(self, RelatedQuestionDomain)
        return domain

