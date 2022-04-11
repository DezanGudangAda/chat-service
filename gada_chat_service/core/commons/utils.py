from datetime import date, datetime, time, timedelta
from typing import Optional
import pytz

from gada_chat_service.core.commons.constant import JAKARTA_UTC_OFFSET_HOURS


class DatetimeUtil:
    JAKARTA_UTC_OFFSET_HOURS = 7

    @staticmethod
    def convert_datetime_to_timestamp(value: datetime) -> int:
        """Return datetime as UTC timestamp"""
        return int(value.timestamp())

    @staticmethod
    def convert_naive_datetime_to_jakarta_time(
        value: Optional[datetime],
    ) -> Optional[datetime]:
        """
        Return naive datetime in jakarta time.
        If input is aware datetime, it will also be converted to naive
        for consistency.
        """

        if not value:
            return None

        if not value.tzinfo:
            return value + timedelta(hours=JAKARTA_UTC_OFFSET_HOURS)

        return (
            value.astimezone(pytz.utc) + timedelta(hours=JAKARTA_UTC_OFFSET_HOURS)
        ).replace(tzinfo=None)
