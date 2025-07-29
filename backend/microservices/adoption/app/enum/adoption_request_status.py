from enum import StrEnum

class AdoptionRequestStatus(StrEnum):
    ACCEPTED = "ACCEPTED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    WITHDREW = "WITHDREW"