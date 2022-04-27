from injector import Injector

from gada_chat_service.chat_service.base_question.modules import BaseQuestionModule
from gada_chat_service.chat_service.channel.modules import ChannelModule
from gada_chat_service.chat_service.getstream.modules import GetStreamModule
from gada_chat_service.chat_service.migrations.modules import ConnectionModule
from gada_chat_service.chat_service.qna_journey.modules import QnaJourneyModule
from gada_chat_service.chat_service.related_answer.modules import RelatedAnswerModule
from gada_chat_service.chat_service.related_question.modules import RelatedQuestionModule
from gada_chat_service.chat_service.user.modules import UserModule

injector = Injector(
    [
        UserModule,
        GetStreamModule,
        ConnectionModule,
        ChannelModule,
        BaseQuestionModule,
        RelatedAnswerModule,
        RelatedQuestionModule,
        QnaJourneyModule,
    ]
)
