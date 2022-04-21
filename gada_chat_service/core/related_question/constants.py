from enum import Enum


class ContextType(Enum):
    PRODUCT = "PRODUCT"
    ORDER = "ORDER"


class TriggerAction(Enum):
    UPDATE_STOCK = "UPDATE STOCK"


PREFIX_CODE = "RQ"
