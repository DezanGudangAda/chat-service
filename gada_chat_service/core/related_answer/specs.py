from dataclasses import dataclass
from typing import Optional

from gada_chat_service.core.related_answer.constants import TriggerAction


@dataclass
class RelatedQuestionResult:
    id: int
    code: str
    answer: str
    trigger_action: Optional[TriggerAction]


@dataclass
class InsertRelatedQuestionSpec:
    code: str
    answer: str
    trigger_action: Optional[TriggerAction]


@dataclass
class CreateRelatedQuestionSpec:
    answer: str
    trigger_action: Optional[TriggerAction]


@dataclass
class GetByCodeSpec:
    code: str
