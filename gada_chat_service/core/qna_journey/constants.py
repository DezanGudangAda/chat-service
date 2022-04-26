from enum import Enum

from gada_chat_service.core.base_question.constants import PREFIX_CODE as BASE_QUESTION_PREFIX_CODE
from gada_chat_service.core.related_answer.constants import PREFIX_CODE as BASE_RELATED_QUESTION_PREFIX_CODE

from gada_chat_service.core.related_question.constants import PREFIX_CODE as RELATED_ANSWER_PREFIX_CODE


class NodeType(Enum):
    BASE_QUESTION = "BASE_QUESTION"
    RELATED_QUESTION = "RELATED_QUESTION"
    RELATED_ANSWER = "RELATED_ANSWER"


class PrefixIdentifier(Enum):
    BASE_QUESTION = BASE_QUESTION_PREFIX_CODE
    RELATED_QUESTION = BASE_RELATED_QUESTION_PREFIX_CODE
    RELATED_ANSWER = RELATED_ANSWER_PREFIX_CODE
