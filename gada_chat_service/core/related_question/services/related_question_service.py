from typing import Optional, List

from fastapi import HTTPException
from injector import inject

from gada_chat_service.core.related_question.specs import RelatedQuestionResult
from gada_chat_service.core.related_question.accessors.related_question_accessor import IRelatedQuestionAccessor
from gada_chat_service.core.related_question.constants import PREFIX_CODE
from gada_chat_service.core.related_question.specs import CreateRelatedQuestionSpec, InsertRelatedQuestionSpec


class RelatedQuestionService:
    @inject
    def __init__(
            self,
            related_question_accessor: IRelatedQuestionAccessor
    ):
        self.related_question_accessor = related_question_accessor

    def _generate_related_question_code(self) -> str:
        code = self.related_question_accessor.get_last_id()
        return f"{PREFIX_CODE}{str(code)}"

    def create(self, spec: CreateRelatedQuestionSpec) -> Optional[RelatedQuestionResult]:
        code = self._generate_related_question_code()

        new_question = self.related_question_accessor.create(InsertRelatedQuestionSpec(
            question=spec.question,
            trigger_action=spec.trigger_action,
            code=code,
            context=spec.context,
            is_automate_reply=spec.is_automate_reply
        ))

        return RelatedQuestionResult(
            trigger_action=new_question.trigger_action,
            code=new_question.code,
            question=new_question.question,
            is_automate_reply=new_question.is_automate_reply,
            context=new_question.context,
            id=new_question.id
        )

    def get_by_code(self, code: str) -> Optional[RelatedQuestionResult]:
        related_question = self.related_question_accessor.get_by_code(code)

        if related_question is None:
            raise HTTPException(detail="related question not found", status_code=404)

        return RelatedQuestionResult(
            question=related_question.question,
            code=related_question.code,
            is_automate_reply=related_question.is_automate_reply,
            context=related_question.context,
            id=related_question.id,
            trigger_action=related_question.trigger_action
        )

    def get_all(self) -> Optional[List[RelatedQuestionResult]]:
        related_questions = self.related_question_accessor.get_all()

        if related_questions is None:
            return None

        result = []

        for related_question in related_questions:
            result.append(RelatedQuestionResult(
                question=related_question.question,
                code=related_question.code,
                is_automate_reply=related_question.is_automate_reply,
                context=related_question.context,
                id=related_question.id,
                trigger_action=related_question.trigger_action
            ))

        return result
