from sqlalchemy import Column, Integer, String, Boolean

from gada_chat_service.chat_service.base.models import Base
from gada_chat_service.core.base_question.models import BaseQuestionDomain
from gada_chat_service.core.commons.utils import ObjectMapperUtil


class BaseQuestion(Base):
    __tablename__ = "base_question"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    is_automate_reply = Column(Boolean)
    context = Column(String)
    code = Column(String)
    trigger_action = Column(String)
    
    def to_domain(self) -> BaseQuestionDomain:
        domain = ObjectMapperUtil.map(self, BaseQuestionDomain)
        return domain
