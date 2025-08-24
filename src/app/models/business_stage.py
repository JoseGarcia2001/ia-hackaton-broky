from enum import Enum


class SellerStage(str, Enum):
    REGISTRATION = "registration"
    PUBLISHING = "publishing" 
    VISITS = "visits"
    COMPLETED = "completed"


class BuyerStage(str, Enum):
    CONTACT = "contact"
    QUALIFICATION = "qualification"
    SCHEDULING = "scheduling" 
    FOLLOW_UP = "follow_up"