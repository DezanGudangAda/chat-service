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
    is_end_of_nodes: bool
