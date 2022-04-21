from dataclasses import dataclass

from gada_chat_service.core.base_question.constants import BaseQuestionContext


@dataclass
class BaseQuestionDomain:
    id: int
    question: str
    is_automate_reply: bool
    context: BaseQuestionContext
    trigger_action: str
    code: str
