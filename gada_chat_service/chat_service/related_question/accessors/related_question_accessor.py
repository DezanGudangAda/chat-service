from typing import Optional, List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from gada_chat_service.chat_service.related_question.models import RelatedQuestion
from gada_chat_service.core.config.services.configuration_service import ConfigurationService
from gada_chat_service.core.related_question.accessors.related_question_accessor import IRelatedQuestionAccessor
from gada_chat_service.core.related_question.models import RelatedQuestionDomain
from gada_chat_service.core.related_question.specs import InsertRelatedQuestionSpec


class RelatedQuestionAccessor(IRelatedQuestionAccessor):
    def __init__(self):
        self.configuration_service = ConfigurationService()
        engine = create_engine(self.configuration_service.get_dsn())
        self._session = Session(bind=engine)
        self._query = self._session.query(RelatedQuestion)

    def create(self, spec: InsertRelatedQuestionSpec) -> Optional[RelatedQuestionDomain]:
        new_related_question = RelatedQuestion()
        new_related_question.question = spec.question
        new_related_question.code = spec.code
        new_related_question.trigger_action = spec.trigger_action.value
        new_related_question.is_automate_reply = spec.is_automate_reply
        new_related_question.context = spec.context.value

        self._session.add(new_related_question)
        self._session.commit()

        return new_related_question.to_domain()

    def get_by_code(self, code: str) -> Optional[RelatedQuestionDomain]:
        related_question = self._query.filter(RelatedQuestion.code == code).first()

        if related_question is None:
            return None

        return related_question.to_domain()

    def get_last_id(self) -> int:
        related_question = self._query.order_by(RelatedQuestion.id.desc()).first()

        if related_question is None:
            return 0

        return related_question.id

    def get_all(self) -> Optional[List[RelatedQuestionDomain]]:
        related_questions = self._query.order_by(RelatedQuestion.id.asc())

        if related_questions is None:
            return None

        result = []
        for question in related_questions:
            result.append(question.to_domain())

        return result