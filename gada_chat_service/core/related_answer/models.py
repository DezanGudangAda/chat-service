from dataclasses import dataclass

from gada_chat_service.core.related_answer.constants import TriggerAction


@dataclass
class RelatedAnswerDomain:
    id: int
    answer: str
    trigger_action: TriggerAction
    code: str

