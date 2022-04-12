from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Any, Dict, TypeVar, Type
import pytz
import dataclasses
from dataclasses import fields

import uuid

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


class DictionaryUtil:
    @staticmethod
    def transform_into_jsonable_dictionary(
            data_object: Dict[str, Any],
            datetime_format: Optional[str] = None,
            is_datetime_in_jakarta_time: bool = True,
    ) -> Optional[Dict[str, Any]]:
        if not isinstance(data_object, Dict):
            return None

        T = TypeVar("T")

        def transform_data(data: T) -> T:
            if isinstance(data, Enum):
                data = data.value
            elif isinstance(data, Decimal):
                data = float(data)
            elif isinstance(data, uuid.UUID):
                data = str(data)
            elif isinstance(data, datetime):
                if datetime_format:
                    data = data.strftime(datetime_format)
                else:
                    data = data.astimezone().isoformat()
            elif isinstance(data, time):
                data = data.isoformat()
            elif isinstance(data, date):
                data = data.isoformat()
            elif isinstance(data, List):
                for index in range(len(data)):
                    data[index] = transform_data(data[index])
            elif isinstance(data, Dict):
                for key in data:
                    data[key] = transform_data(data[key])
            elif dataclasses.is_dataclass(data):
                data = transform_data(dataclasses.asdict(data))

            return data

        return transform_data(data_object)

    @staticmethod
    def transform_into_jsonable_array(
            data_array: List[Any], datetime_format: Optional[str] = None
    ) -> Optional[List[Any]]:
        results = []
        for data_object in data_array:
            if dataclasses.is_dataclass(data_object):
                data_object = dataclasses.asdict(data_object)

            results.append(
                DictionaryUtil.transform_into_jsonable_dictionary(
                    data_object, datetime_format
                )
            )

        return results


class ObjectMapperUtil:
    T = TypeVar("T")

    @staticmethod
    def map(source_model_object, destination_domain_class: Type[T]) -> T:
        """
        This method will not raise error if the source object does not have attribute(s)
        required by the destination domain class.
        """
        domain_fields = [field.name for field in fields(destination_domain_class)]
        if issubclass(type(source_model_object), dict):
            attributes = {
                field: source_model_object.get(field) for field in domain_fields
            }
        else:
            attributes = {
                field: getattr(source_model_object, field, None)
                for field in domain_fields
            }
        return destination_domain_class(**attributes)