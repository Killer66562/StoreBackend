from enum import Enum


class Gender(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class OrderStatus(Enum):
    NOT_DELIVERED = 1
    DELIVERED = 2
    PROCESSING = 3
    ARRIVED = 4
    DONE = 5