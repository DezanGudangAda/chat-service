from typing import Optional

from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session

from gada_chat_service.chat_service.qna_journey.models import QnaJourney
from gada_chat_service.core.qna_journey.accessors.qna_journey_accessor import IQnaJourneyAccessor
from gada_chat_service.core.qna_journey.models import QnaJourneyDomain
from gada_chat_service.core.qna_journey.specs import RelatedNodesResult, UpdatePathSpec


class QnaJourneyAccessor(IQnaJourneyAccessor):
    def __init__(self):
        engine = create_engine("postgresql+psycopg2://postgres:AdminPassword123@localhost/chat-service")
        self._session = Session(bind=engine)
        self._query = self._session.query(QnaJourney)

    def create(self, nodes: str) -> QnaJourneyDomain:
        new_journey = QnaJourney()
        new_journey.path = nodes

        self._session.add(new_journey)
        self._session.commit()

        return new_journey.to_domain()

    def get_related_nodes(self, nodes: str) -> Optional[RelatedNodesResult]:
        nodes = self._query.filter(QnaJourney.path.like(f'{nodes}%')).all()

        if nodes is None:
            return None

        result = []
        for node in nodes:
            result.append(node.path)

        return RelatedNodesResult(
            nodes=result
        )

    def append_node_to_journey(self, spec: UpdatePathSpec) -> Optional[QnaJourneyDomain]:
        current_journey = self._query.filter(
            QnaJourney.id == spec.journey_id
        ).first()

        if current_journey is None:
            return None

        current_journey.path = spec.new_path
        self._session.commit()

        return current_journey.to_domain()

    def get_by_id(self, journey_id: int) -> Optional[QnaJourneyDomain]:
        current_journey = self._query.filter(
            QnaJourney.id == journey_id
        ).first()

        if current_journey is None:
            return None

        return current_journey.to_domain()