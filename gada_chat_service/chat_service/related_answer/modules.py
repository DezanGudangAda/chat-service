from injector import Module, Binder, singleton

from gada_chat_service.chat_service.related_answer.accessors.related_answer_accessor import RelatedAnswerAccessor
from gada_chat_service.core.related_answer.accessors.related_answer_accessor import IRelatedAnswerAccessor
from gada_chat_service.core.related_answer.services.related_answer_service import RelatedAnswerService


class RelatedAnswerModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            IRelatedAnswerAccessor,
            to=RelatedAnswerAccessor,
            scope=singleton,
        )
        binder.bind(
            RelatedAnswerService,
            to=RelatedAnswerService,
            scope=singleton,
        )