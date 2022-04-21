from typing import Optional, List

from fastapi import HTTPException
from injector import inject

from gada_chat_service.core.base_question.accessor.base_question_accessor import IBaseQuestionAccessor
from gada_chat_service.core.base_question.constants import PREFIX_CODE
from gada_chat_service.core.base_question.specs import CreateBaseQuestionSpec, BaseQuestionResult, \
    InsertBaseQuestionSpec, GetByContextSpec


class BaseQuestionService:
    @inject
    def __init__(
            self,
            base_question_accessor: IBaseQuestionAccessor
    ):
        self.base_question_accessor = base_question_accessor

    def _generate_code_base_question(self) -> str:
        last_id = self.base_question_accessor.get_last_id()
        return f"{PREFIX_CODE}{str(last_id)}"

    def create(self, spec: CreateBaseQuestionSpec) -> Optional[BaseQuestionResult]:
        code = self._generate_code_base_question()

        new_question = self.base_question_accessor.create(InsertBaseQuestionSpec(
            question=spec.question,
            code=code,
            context=spec.context
        ))

        return BaseQuestionResult(
            question=new_question.question,
            context=new_question.context,
            code=new_question.code,
            id=new_question.id
        )

    def get_by_context(self, spec: GetByContextSpec) -> Optional[List[BaseQuestionResult]]:
        questions = self.base_question_accessor.get_by_context(spec.context)

        if questions is None:
            raise HTTPException(status_code=404, detail="not question yet")

        result = []
        for question in questions:
            result.append(
                BaseQuestionResult(
                    question=question.question,
                    context=question.context,
                    code=question.code,
                    id=question.id,
                )
            )

        return result

    def get_by_code(self, code: str) -> Optional[BaseQuestionResult]:
        question = self.base_question_accessor.get_by_code(code)

        if question is None:
            raise HTTPException(status_code=404, detail="question not found")

        return BaseQuestionResult(
            question=question.question,
            code=question.code,
            context=question.context,
            id=question.id,
        )
