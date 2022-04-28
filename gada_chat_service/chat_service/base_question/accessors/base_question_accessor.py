from typing import Optional, List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from gada_chat_service.chat_service.base_question.models import BaseQuestion
from gada_chat_service.core.base_question.accessors.base_question_accessor import IBaseQuestionAccessor
from gada_chat_service.core.base_question.constants import BaseQuestionContext
from gada_chat_service.core.base_question.models import BaseQuestionDomain
from gada_chat_service.core.base_question.specs import InsertBaseQuestionSpec


class BaseQuestionAccessor(IBaseQuestionAccessor):
    def __init__(self):
        engine = create_engine("postgresql+psycopg2://postgres:AdminPassword123@localhost/chat-service")
        self._session = Session(bind=engine)
        self._query = self._session.query(BaseQuestion)

    def create(self, spec: InsertBaseQuestionSpec) -> BaseQuestionDomain:
        new_base_question = BaseQuestion()
        new_base_question.question = spec.question
        new_base_question.code = spec.code
        new_base_question.context = spec.context.value
        # TODO: Add to spec
        new_base_question.is_automate_reply = False
        new_base_question.trigger_action = ""

        self._session.add(new_base_question)
        self._session.commit()

        return new_base_question.to_domain()

    def get_by_code(self, code: str) -> Optional[BaseQuestionDomain]:
        base_question = self._query.filter(
            BaseQuestion.code == code
        )

        if base_question is None:
            return None

        return base_question.to_domain()

    def get_by_id(self, id_base: int) -> Optional[BaseQuestionDomain]:
        base_question = self._query.filter(
            BaseQuestion.id == id_base
        )

        if base_question is None:
            return None

        return base_question.to_domain()

    def get_last_id(self) -> int:
        base_question = self._query.order_by(BaseQuestion.id.desc()).first()

        if base_question is None:
            return 0

        return base_question.id

    def get_by_context(self, spec: BaseQuestionContext) -> Optional[List[BaseQuestionDomain]]:
        base_question = self._query.filter(
            BaseQuestion.context == spec.value
        )

        if base_question is None:
            return None

        result = []
        for base in base_question:
            result.append(base.to_domain())

        return result

    def get_all(self) -> Optional[List[BaseQuestionDomain]]:
        base_question = self._query.order_by(BaseQuestion.id.desc())

        if base_question is None:
            return None

        result = []
        for base in base_question:
            result.append(base.to_domain())

        return result
