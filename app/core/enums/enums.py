from enum import Enum


class RequestStatus(Enum):
    PENDING: str = "pending"
    ACCEPTED: str = "accepted"
    REJECTED: str = "rejected"


class AdType(Enum):
    SERVICE: str = "service"
    ITEM: str = "item"


class Currency(Enum):
    EUR: str = "€"
    GBP: str = "£"
    USD: str = "$"
