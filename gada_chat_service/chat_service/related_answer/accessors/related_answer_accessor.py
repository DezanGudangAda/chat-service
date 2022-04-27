from typing import Optional, List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from gada_chat_service.chat_service.related_answer.models import RelatedAnswer
from gada_chat_service.core.related_answer.accessors.related_answer_accessor import IRelatedAnswerAccessor
from gada_chat_service.core.related_answer.models import RelatedAnswerDomain
from gada_chat_service.core.related_answer.specs import InsertRelatedAnswerSpec


class RelatedAnswerAccessor(IRelatedAnswerAccessor):
    def __init__(self):
        engine = create_engine("postgresql+psycopg2://postgres:AdminPassword123@localhost/chat-service")
        self._session = Session(bind=engine)
        self._query = self._session.query(RelatedAnswer)

    def create(self, spec: InsertRelatedAnswerSpec) -> Optional[RelatedAnswerDomain]:
        new_related_answer = RelatedAnswer()
        new_related_answer.answer = spec.answer
        new_related_answer.code = spec.code
        new_related_answer.trigger_action = spec.trigger_action.value

        self._session.add(new_related_answer)
        self._session.commit()

        return new_related_answer.to_domain()

    def get_by_code(self, code: str) -> Optional[RelatedAnswerDomain]:
        related_answer = self._query.filter(
            RelatedAnswer.code == code
        ).first()

        if related_answer is None:
            return None

        return related_answer.to_domain()

    def get_all(self) -> Optional[List[RelatedAnswerDomain]]:
        related_answer = self._query.order_by(RelatedAnswer.id)

        if related_answer is None:
            return None

        result = []
        for ans in related_answer:
            result.append(ans.to_domain())

        return result

    def get_last_id(self) -> int:
        related_answer = self._query.order_by(RelatedAnswer.id.desc()).first()

        if related_answer is None:
            return 0

        return related_answer.id
