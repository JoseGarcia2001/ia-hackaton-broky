from enum import Enum


class SellerStage(str, Enum):
    """
    Estados validos para el tipo de usuario seller
    """
    REGISTRATION = "registration"
    PUBLISHING = "publishing" 
    VISITS = "visits"
    COMPLETED = "completed"


class BuyerStage(str, Enum):
    """
    Estados validos para el tipo de usuario buyer
    """
    CONTACT = "contact"
    QUALIFICATION = "qualification"
    SCHEDULING = "scheduling" 
    FOLLOW_UP = "follow_up"