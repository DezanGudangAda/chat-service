from dataclasses import dataclass
from typing import Optional, List

from gada_chat_service.core.qna_journey.constants import NodeType


@dataclass
class NodeResult:
    text: str
    node_type: NodeType
    code: str


@dataclass
class GetNextNodesSpec:
    current_path: str


@dataclass
class GetNextNodesResult:
    nodes: Optional[List[NodeResult]]


@dataclass
class AppendNewNodeSpec:
    id: int
    before_node_code: Optional[str] # RA0
    node_code: str #


@dataclass
class CreateJourneySpec:
    nodes: List[str]


@dataclass
class RelatedNodesResult:
    nodes: Optional[List[str]]

@dataclass
class UpdatePathSpec:
    new_path: str
    journey_id: id