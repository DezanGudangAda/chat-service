from typing import Optional, List

from fastapi import HTTPException
from injector import inject

from gada_chat_service.core.related_answer.accessors.related_answer_accessor import IRelatedAnswerAccessor
from gada_chat_service.core.related_answer.constant import PREFIX_CODE
from gada_chat_service.core.related_answer.specs import RelatedQuestionResult, CreateRelatedQuestionSpec, \
    InsertRelatedQuestionSpec, GetByCodeSpec


class RelatedAnswerService:
    @inject
    def __init__(
            self,
            related_answer_accessor: IRelatedAnswerAccessor
    ):
        self.related_answer_accessor = related_answer_accessor

    def _generate_code_related_answer(self) -> str:
        code = self.related_answer_accessor.get_last_id()
        return f"{PREFIX_CODE}{code}"

    def create(self, spec: CreateRelatedQuestionSpec) -> Optional[RelatedQuestionResult]:
        code = self._generate_code_related_answer()

        new_related_answer = self.related_answer_accessor.create(InsertRelatedQuestionSpec(
            answer=spec.answer,
            code=code,
            trigger_action=spec.trigger_action,
        ))

        return RelatedQuestionResult(
            trigger_action=new_related_answer.trigger_action,
            answer=new_related_answer.answer,
            code=new_related_answer.code,
            id=new_related_answer.id
        )

    def get_by_code(self, spec: GetByCodeSpec) -> Optional[RelatedQuestionResult]:
        related_answer = self.related_answer_accessor.get_by_code(spec.code)

        if related_answer is None:
            raise HTTPException(status_code=404, detail="related answer not found")

        return RelatedQuestionResult(
            trigger_action=related_answer.trigger_action,
            answer=related_answer.answer,
            code=related_answer.code,
            id=related_answer.id
        )

    def get_all(self) -> Optional[List[RelatedQuestionResult]]:
        related_answers = self.related_answer_accessor.get_all()

        if related_answers is None:
            return None

        result = []
        for answer in related_answers:
            result.append(
                RelatedQuestionResult(
                    trigger_action=answer.trigger_action,
                    id=answer.id,
                    code=answer.code,
                    answer=answer.answer
                )
            )

        return result
