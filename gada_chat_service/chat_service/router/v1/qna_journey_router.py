from fastapi import APIRouter

from gada_chat_service.chat_service.injector import injector
from gada_chat_service.core.qna_journey.services.qna_journey_service import QnaJourneyService
from gada_chat_service.core.qna_journey.specs import CreateJourneySpec, GetNextNodesSpec

qna_journey_service: QnaJourneyService = injector.get(
    QnaJourneyService
)

qna_journey_router = APIRouter(
    prefix="/qna-journey",
    tags=["QNA Journey"],
)


@qna_journey_router.post("")
async def create_journey(spec: CreateJourneySpec):
    res = qna_journey_service.create(spec)

    return {
        "data": res,
        "message": "succeed"
    }


@qna_journey_router.get("/next-nodes")
async def get_next_nodes(path: str = ""):
    res = qna_journey_service.get_next_nodes(GetNextNodesSpec(
        current_path=path
    ))

    return {
        "data": res,
        "message": "succeed"
    }


@qna_journey_router.get("")
async def get_all_qna_journey():
    res = qna_journey_service.get_all()

    return {
        "data": res,
        "message": "succeed"
    }
