from enum import Enum


class UserType(Enum):
    SELLER = "SELLER"
    BUYER = "BUYER"


class ContextType(Enum):
    PRODUCT = "PRODUCT"
    ORDER = "ORDER"
