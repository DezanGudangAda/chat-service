from dataclasses import dataclass
from typing import Optional

from gada_chat_service.core.related_answer.constants import TriggerAction


@dataclass
class RelatedAnswerResult:
    id: int
    code: str
    answer: str
    trigger_action: Optional[TriggerAction]


@dataclass
class InsertRelatedAnswerSpec:
    code: str
    answer: str
    trigger_action: Optional[TriggerAction]


@dataclass
class CreateRelatedAnswerSpec:
    answer: str
    trigger_action: Optional[TriggerAction]


@dataclass
class GetByCodeSpec:
    code: str
