from fastapi import APIRouter

from gada_chat_service.chat_service.injector import injector
from gada_chat_service.core.related_answer.services.related_answer_service import RelatedAnswerService
from gada_chat_service.core.related_answer.specs import CreateRelatedAnswerSpec, GetByCodeSpec
from gada_chat_service.core.related_question.services.related_question_service import RelatedQuestionService
from gada_chat_service.core.related_question.specs import CreateRelatedQuestionSpec

related_question_service: RelatedQuestionService = injector.get(
    RelatedQuestionService
)

related_question_router = APIRouter(
    prefix="/related-question",
    tags=["Related Question"],
)


@related_question_router.post("")
async def create_related_answer(spec: CreateRelatedQuestionSpec):
    res = related_question_service.create(spec)

    return {
        "data": res,
        "message": "succeed"
    }


@related_question_router.get("")
async def fetch_all_related_data_record():
    res = related_question_service.get_all()

    return {
        "data": res,
        "message": "succeed"
    }


@related_question_router.get("/{code}")
async def get_by_code(code: str = ""):
    res = related_question_service.get_by_code(code)

    return {
        "data": res,
        "message": "succeed"
    }
