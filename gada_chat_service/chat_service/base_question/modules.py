from injector import Module, Binder, singleton

from gada_chat_service.chat_service.base_question.accessors.base_question_accessor import BaseQuestionAccessor
from gada_chat_service.core.base_question.accessors.base_question_accessor import IBaseQuestionAccessor
from gada_chat_service.core.base_question.services.base_question_service import BaseQuestionService


class BaseQuestionModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            IBaseQuestionAccessor,
            to=BaseQuestionAccessor,
            scope=singleton,
        )
        binder.bind(
            BaseQuestionService,
            to=BaseQuestionService,
            scope=singleton,
        )