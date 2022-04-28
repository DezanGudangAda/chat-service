import json
from typing import Optional, List, Dict

from fastapi import HTTPException
from injector import inject

from gada_chat_service.core.base_question.services.base_question_service import BaseQuestionService
from gada_chat_service.core.qna_journey.accessors.qna_journey_accessor import IQnaJourneyAccessor
from gada_chat_service.core.qna_journey.constants import NodeType, PrefixIdentifier
from gada_chat_service.core.qna_journey.models import QnaJourneyDomain
from gada_chat_service.core.qna_journey.specs import CreateJourneySpec, GetNextNodesSpec, GetNextNodesResult, \
    NodeResult, AppendNewNodeSpec, UpdatePathSpec
from gada_chat_service.core.related_answer.services.related_answer_service import RelatedAnswerService
from gada_chat_service.core.related_answer.specs import GetByCodeSpec
from gada_chat_service.core.related_question.services.related_question_service import RelatedQuestionService


class QnaJourneyService:
    @inject
    def __init__(
            self,
            qna_journey_accessor: IQnaJourneyAccessor,
            base_question_service: BaseQuestionService,
            related_question_service: RelatedQuestionService,
            related_answer_service: RelatedAnswerService,
    ):
        self.related_answer_service = related_answer_service
        self.related_question_service = related_question_service
        self.base_question_service = base_question_service
        self.qna_journey_accessor = qna_journey_accessor

    def _check_node_type(self, node: str) -> Optional[NodeType]:
        if node.startswith(PrefixIdentifier.BASE_QUESTION.value):
            return NodeType.BASE_QUESTION

        if node.startswith(PrefixIdentifier.RELATED_ANSWER.value):
            return NodeType.RELATED_ANSWER

        if node.startswith(PrefixIdentifier.RELATED_QUESTION.value):
            return NodeType.RELATED_QUESTION

        return None

    def create(self, spec: CreateJourneySpec) -> Optional[QnaJourneyDomain]:
        if self._check_node_type(spec.nodes[0]) != NodeType.BASE_QUESTION:
            raise HTTPException(status_code=400, detail="First question should be base question")

        journey = self.qna_journey_accessor.create("/".join(spec.nodes))

        return journey

    def _get_base_question(self, code: str) -> Optional[str]:
        question = self.base_question_service.get_by_code(code)
        if question is None:
            raise HTTPException(status_code=400, detail=f"{code} Question not found")

        return question.question

    def _get_related_answer(self, code: str) -> Optional[str]:
        related_answer = self.related_answer_service.get_by_code(GetByCodeSpec(
            code=code
        ))
        if related_answer is None:
            raise HTTPException(status_code=400, detail=f"{code} Related Answer not found")

        return related_answer.answer

    def _get_related_question(self, code: str) -> Optional[str]:
        related_question = self.related_question_service.get_by_code(code)
        if related_question is None:
            raise HTTPException(status_code=400, detail=f"{code} Related Answer not found")

        return related_question.question

    def _get_next_node_orchestrator(self, node: str) -> Optional[NodeResult]:
        node_type = self._check_node_type(node)
        text = ""

        if node_type is None:
            raise HTTPException(status_code=400, detail="question or answer is not valid")

        if node_type == node_type.BASE_QUESTION:
            text = self._get_base_question(node)

        if node_type == node_type.RELATED_ANSWER:
            text = self._get_related_answer(node)

        if node_type == node_type.RELATED_QUESTION:
            text = self._get_related_question(node)

        return NodeResult(
            node_type=node_type.value,
            text=text,
            code=node,
        )

    # TODO: Add validation in get next nodes
    # TODO: Add rate limit (setiap 5 menit)
    # TODO: Full text chat in channel
    def get_next_nodes(self, spec: GetNextNodesSpec) -> Optional[GetNextNodesResult]:
        next_nodes = self.qna_journey_accessor.get_related_nodes(spec.current_path)

        if len(next_nodes.nodes) == 1 and next_nodes.nodes[0] == spec.current_path:
            return GetNextNodesResult(
                nodes=[]
            )

        trimmed_nodes = []
        for node in next_nodes.nodes:
            trimmed_nodes.append(node.replace(f"{spec.current_path}/", ""))

        result = []
        checker = {}
        for node in trimmed_nodes:
            split_node = node.split("/", 1)
            if checker.get(split_node[0]) is not True:
                get_detail_node = self._get_next_node_orchestrator(split_node[0])
                result.append(get_detail_node)
                checker[split_node[0]] = True

        return GetNextNodesResult(
            nodes=result
        )

    def append_nodes(self, spec: AppendNewNodeSpec):
        journey = self.qna_journey_accessor.get_by_id(spec.id)
        path = journey.path
        if journey is None:
            raise HTTPException(status_code=404, detail="journey not found")

        if spec.before_node_code is not None:
            split_path = path.split("/")
            found = False

            if split_path == 0:
                raise HTTPException(status_code=400, detail="journey not valid, you need append the head of node first")

            for i, node_code in enumerate(split_path):
                if node_code == spec.before_node_code:
                    found = True
                    break

            if not found:
                raise HTTPException(status_code=400, detail="before node is not found in the path journey")

            split_path.insert(split_path.index(spec.before_node_code) + 1, spec.node_code)
            path = "/".join(split_path)

        elif spec.before_node_code is None:
            path = f"{spec.node_code}/"

        self.qna_journey_accessor.append_node_to_journey(UpdatePathSpec(
            journey_id=spec.id,
            new_path=path
        ))

        return

    def get_all(self) -> Optional[List[QnaJourneyDomain]]:
        qna_journeys = self.qna_journey_accessor.get_all()
        return qna_journeys
