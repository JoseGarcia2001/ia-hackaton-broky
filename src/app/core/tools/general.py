"""
Defines the tools for the general purposes
"""

from typing import Annotated
from langchain.tools import tool
from enum import Enum
from langgraph.prebuilt import InjectedState


class SellerBusinessStage(Enum):
    REGISTRATION = "regist"
    PUBLISH = "publish"
    VISITS = "visits"


class BuyerBusinessStage(Enum):
    SCHEDULE = "schedule"


@tool
def update_business_stage(
    stage: SellerBusinessStage | BuyerBusinessStage, state: Annotated[dict, InjectedState]
) -> str:
    """
    Update the business stage of the company.
    """
    return f"Business stage updated to {stage}"
