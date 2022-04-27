from injector import Module, Binder, singleton

from gada_chat_service.chat_service.related_question.accessors.related_question_accessor import RelatedQuestionAccessor
from gada_chat_service.core.related_question.accessors.related_question_accessor import IRelatedQuestionAccessor
from gada_chat_service.core.related_question.services.related_question_service import RelatedQuestionService


class RelatedQuestionModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            IRelatedQuestionAccessor,
            to=RelatedQuestionAccessor,
            scope=singleton,
        )
        binder.bind(
            RelatedQuestionService,
            to=RelatedQuestionService,
            scope=singleton,
        )