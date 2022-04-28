from abc import ABC, abstractmethod
from typing import Optional, List

from gada_chat_service.core.qna_journey.models import QnaJourneyDomain
from gada_chat_service.core.qna_journey.specs import RelatedNodesResult, UpdatePathSpec


class IQnaJourneyAccessor(ABC):
    @abstractmethod
    def create(self, nodes: str) -> QnaJourneyDomain:
        raise NotImplementedError

    @abstractmethod
    def get_related_nodes(self, nodes: str) -> Optional[RelatedNodesResult]:
        raise NotImplementedError

    @abstractmethod
    def append_node_to_journey(self, spec: UpdatePathSpec) -> Optional[QnaJourneyDomain]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, journey_id: int) -> Optional[QnaJourneyDomain]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Optional[List[QnaJourneyDomain]]:
        raise NotImplementedError
