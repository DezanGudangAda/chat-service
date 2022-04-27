from injector import Module, singleton, Binder

from gada_chat_service.chat_service.qna_journey.accessors.qna_journey_accessor import QnaJourneyAccessor
from gada_chat_service.core.qna_journey.accessors.qna_journey_accessor import IQnaJourneyAccessor
from gada_chat_service.core.qna_journey.services.qna_journey_service import QnaJourneyService


class QnaJourneyModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            IQnaJourneyAccessor,
            to=QnaJourneyAccessor,
            scope=singleton,
        )
        binder.bind(
            QnaJourneyService,
            to=QnaJourneyService,
            scope=singleton,
        )
