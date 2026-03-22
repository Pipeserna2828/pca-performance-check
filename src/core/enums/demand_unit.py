from enum import Enum


class DemandUnit(str, Enum):
    TPS = "TPS"
    TX_HOUR = "TX_HOUR"
    CONCURRENT_USERS = "CONCURRENT_USERS"
