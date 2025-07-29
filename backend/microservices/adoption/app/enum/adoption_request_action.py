from enum import StrEnum

class AdoptionRequestAction(StrEnum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    WITHDRAW = "WITHDRAW"