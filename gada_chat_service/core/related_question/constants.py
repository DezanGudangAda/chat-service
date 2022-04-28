from enum import Enum


class ContextType(Enum):
    GENERAL = "GENERAL"
    PRODUCT = "PRODUCT"
    ORDER = "ORDER"


class TriggerAction(Enum):
    NONE = "NONE"
    UPDATE_STOCK = "UPDATE STOCK"


PREFIX_CODE = "RQ"
