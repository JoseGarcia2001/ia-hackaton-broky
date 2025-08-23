from app.core.agent.main import Agent
from app.core.agent.seller.register import RegisterAgent
from app.core.agent.seller.publisher import PublisherAgent
from app.core.agent.seller.visits import VisitsAgent
from app.core.agent.buyer.scheduler import SchedulerAgent


class AgentsFactory:
    @staticmethod
    def seller_agent() -> Agent:
        """
        Defines rules to get a specific agent for a seller.
        """
        # TODO: Get the stage of the seller
        stage = "regist"
        mapped_stage = {
            None: RegisterAgent,
            "regist": RegisterAgent,
            "publish": PublisherAgent,
            "visits": VisitsAgent
        }
        return mapped_stage[stage]()

    @staticmethod
    def buyer_agent() -> Agent:
        """
        Defines rules to get a specific agent for a buyer.
        """
        # TODO: Get the stage of the buyer
        stage = "regist"
        mapped_stage = {
            "schedule": SchedulerAgent
        }
        return mapped_stage[stage]()

    @staticmethod
    def get_agent(user_type: str) -> Agent:
        """
        Gets the agent for a specific user type.
        """
        if user_type == "seller":
            return AgentsFactory.seller_agent()
        elif user_type == "buyer":
            return AgentsFactory.buyer_agent()
        else:
            raise ValueError(f"Invalid user type: {user_type}")
