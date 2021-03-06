from fastapi import APIRouter

from gada_chat_service.chat_service.router.v1.base_question_router import base_question_router
from gada_chat_service.chat_service.router.v1.channel_router import channel_router
from gada_chat_service.chat_service.router.v1.qna_journey_router import qna_journey_router
from gada_chat_service.chat_service.router.v1.related_answer_router import related_answer_router
from gada_chat_service.chat_service.router.v1.related_question_router import related_question_router
from gada_chat_service.chat_service.router.v1.template_router import template_router
from gada_chat_service.chat_service.router.v1.user_router import user_router

v1_router = APIRouter(
    prefix="/v1",
)

v1_router.include_router(channel_router)
v1_router.include_router(user_router)
v1_router.include_router(qna_journey_router)
v1_router.include_router(template_router)
v1_router.include_router(base_question_router)
v1_router.include_router(related_answer_router)
v1_router.include_router(related_question_router)