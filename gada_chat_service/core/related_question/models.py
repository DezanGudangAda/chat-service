from dataclasses import dataclass

from gada_chat_service.core.related_question.constants import TriggerAction, ContextType


@dataclass
class RelatedQuestionDomain:
    id: int
    question: str
    is_automate_reply: bool
    trigger_action: TriggerAction
    code: str
    context: ContextType
