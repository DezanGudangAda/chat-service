from abc import ABC, abstractmethod
from typing import Optional, List

from gada_chat_service.core.base_question.constants import BaseQuestionContext
from gada_chat_service.core.base_question.models import BaseQuestionDomain
from gada_chat_service.core.base_question.specs import InsertBaseQuestionSpec


class IBaseQuestionAccessor(ABC):
    @abstractmethod
    def create(self, spec: InsertBaseQuestionSpec) -> BaseQuestionDomain:
        raise NotImplementedError

    def get_by_code(self, code: str) -> Optional[BaseQuestionDomain]:
        raise NotImplementedError

    def get_by_id(self, id_base: int) -> Optional[BaseQuestionDomain]:
        raise NotImplementedError

    def get_last_id(self) -> int:
        raise NotImplementedError

    def get_by_context(self, spec: BaseQuestionContext) -> Optional[List[BaseQuestionDomain]]:
        raise NotImplementedError
