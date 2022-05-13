from fastapi import APIRouter

from gada_chat_service.chat_service.injector import injector
from gada_chat_service.core.base_question.constants import BaseQuestionContext
from gada_chat_service.core.base_question.services.base_question_service import BaseQuestionService
from gada_chat_service.core.base_question.specs import GetByContextSpec

base_question_service: BaseQuestionService = injector.get(
    BaseQuestionService
)

template_router = APIRouter(
    prefix="/template",
    tags=["Template Question"],
)


@template_router.get("/base-question")
async def create_base_question(context: BaseQuestionContext):
    res = base_question_service.get_by_context(GetByContextSpec(
        context=context
    ))

    return {
        "data": res,
        "message": "succeed"
    }


@template_router.get("/base-question/all")
async def create_base_question():
    res = base_question_service.get_all()

    return {
        "data": res,
        "message": "succeed"
    }
