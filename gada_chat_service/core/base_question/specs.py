from dataclasses import dataclass

from gada_chat_service.core.base_question.constants import BaseQuestionContext


@dataclass
class InsertBaseQuestionSpec:
    question: str
    context: BaseQuestionContext
    code: str


@dataclass
class CreateBaseQuestionSpec:
    question: str
    context: BaseQuestionContext


@dataclass
class BaseQuestionResult:
    question: str
    context: BaseQuestionContext
    code: str
    id: int


@dataclass
class GetByContextSpec:
    context: BaseQuestionContext

