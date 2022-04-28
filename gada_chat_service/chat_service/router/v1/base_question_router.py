from fastapi import APIRouter

from gada_chat_service.chat_service.injector import injector
from gada_chat_service.core.base_question.constants import BaseQuestionContext
from gada_chat_service.core.base_question.services.base_question_service import BaseQuestionService
from gada_chat_service.core.base_question.specs import CreateBaseQuestionSpec, GetByContextSpec

base_question_service: BaseQuestionService = injector.get(
    BaseQuestionService
)

base_question_router = APIRouter(
    prefix="/base-question",
    tags=["Base Question"],
)


@base_question_router.post("")
async def create_base_question(spec: CreateBaseQuestionSpec):
    res = base_question_service.create(spec)

    return {
        "data": res,
        "message": "succeed"
    }


@base_question_router.get("/context")
async def create_base_question(context: BaseQuestionContext):
    res = base_question_service.get_by_context(GetByContextSpec(
        context=context
    ))

    return {
        "data": res,
        "message": "succeed"
    }


@base_question_router.get("")
async def get_all_base_questions():
    res = base_question_service.get_all()

    return {
        "data": res,
        "message": "succeed"
    }
