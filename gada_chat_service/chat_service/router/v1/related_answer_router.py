from fastapi import APIRouter

from gada_chat_service.chat_service.injector import injector
from gada_chat_service.core.related_answer.services.related_answer_service import RelatedAnswerService
from gada_chat_service.core.related_answer.specs import CreateRelatedAnswerSpec, GetByCodeSpec

related_answer_service: RelatedAnswerService = injector.get(
    RelatedAnswerService
)

related_answer_router = APIRouter(
    prefix="/related-answer",
    tags=["Related Answer"],
)


@related_answer_router.post("")
async def create_related_answer(spec: CreateRelatedAnswerSpec):
    res = related_answer_service.create(spec)

    return {
        "data": res,
        "message": "succeed"
    }


@related_answer_router.get("")
async def fetch_all_related_data_record():
    res = related_answer_service.get_all()

    return {
        "data": res,
        "message": "succeed"
    }


@related_answer_router.get("/{code}")
async def get_by_code(code: str = ""):
    res = related_answer_service.get_by_code(GetByCodeSpec(
        code=code,
    ))

    return {
        "data": res,
        "message": "succeed"
    }
