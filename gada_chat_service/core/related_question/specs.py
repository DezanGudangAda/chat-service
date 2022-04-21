from dataclasses import dataclass

from gada_chat_service.core.related_question.constants import TriggerAction, ContextType


@dataclass
class RelatedQuestionResult:
    id: int
    question: str
    is_automate_reply: bool
    trigger_action: TriggerAction
    context: ContextType
    code: str


@dataclass
class GetByCodeSpec:
    code: str


@dataclass
class InsertRelatedQuestionSpec:
    question: str
    is_automate_reply: bool
    trigger_action: TriggerAction
    context: ContextType
    code: str


@dataclass
class CreateRelatedQuestionSpec:
    question: str
    is_automate_reply: bool
    trigger_action: TriggerAction
    context: ContextType
