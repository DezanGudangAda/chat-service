from abc import ABC, abstractmethod
from typing import Optional, List

from gada_chat_service.core.related_answer.models import RelatedAnswerDomain
from gada_chat_service.core.related_answer.specs import InsertRelatedAnswerSpec


class IRelatedAnswerAccessor(ABC):
    @abstractmethod
    def create(self, spec: InsertRelatedAnswerSpec) -> Optional[RelatedAnswerDomain]:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[RelatedAnswerDomain]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Optional[List[RelatedAnswerDomain]]:
        raise NotImplementedError

    @abstractmethod
    def get_last_id(self) -> int:
        raise NotImplementedError
