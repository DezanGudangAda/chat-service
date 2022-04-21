from abc import ABC, abstractmethod
from typing import Optional, List

from gada_chat_service.core.related_question.models import RelatedQuestionDomain
from gada_chat_service.core.related_question.specs import InsertRelatedQuestionSpec


class IRelatedQuestionAccessor(ABC):
    @abstractmethod
    def create(self, spec: InsertRelatedQuestionSpec) -> Optional[RelatedQuestionDomain]:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[RelatedQuestionDomain]:
        raise NotImplementedError

    @abstractmethod
    def get_last_id(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Optional[List[RelatedQuestionDomain]]:
        raise NotImplementedError
