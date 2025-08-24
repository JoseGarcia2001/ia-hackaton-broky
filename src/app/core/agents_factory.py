from src.app.core.agent.main import Agent
from src.app.core.agent.seller.register import RegisterAgent
from src.app.core.agent.seller.publisher import PublisherAgent
from src.app.core.agent.seller.visits import VisitsAgent
from src.app.core.agent.buyer.scheduler import SchedulerAgent
from src.app.services.stage_service import StageService
from src.app.models.business_stage import SellerStage, BuyerStage


class AgentsFactory:
    @staticmethod
    def seller_agent(context: dict) -> Agent:
        """
        Defines rules to get a specific agent for a seller.
        """
        chat_id = context.get("chat_id")
        
        stage_service = StageService()
        property_stage = stage_service.get_seller_stage(chat_id)
        
        mapped_stage = {
            SellerStage.REGISTRATION: RegisterAgent,
            SellerStage.PUBLISHING: PublisherAgent,
            SellerStage.VISITS: VisitsAgent,
            SellerStage.COMPLETED: VisitsAgent
        }
        return mapped_stage.get(property_stage, RegisterAgent)()

    @staticmethod
    def buyer_agent(context: dict) -> Agent:
        """
        Defines rules to get a specific agent for a buyer.
        """
        chat_id = context.get("chat_id")
        
        stage_service = StageService()
        buyer_stage = stage_service.get_buyer_stage(chat_id)
        
        mapped_stage = {
            BuyerStage.CONTACT: SchedulerAgent,
            BuyerStage.QUALIFICATION: SchedulerAgent,
            BuyerStage.SCHEDULING: SchedulerAgent,
            BuyerStage.FOLLOW_UP: SchedulerAgent
        }
        return mapped_stage.get(buyer_stage, SchedulerAgent)()

    @staticmethod
    def get_agent(user_type: str, context: dict = None) -> Agent:
        """
        Gets the agent for a specific user type.
        """
        if context is None:
            context = {}
            
        if user_type == "seller":
            return AgentsFactory.seller_agent(context)
        elif user_type == "buyer":
            return AgentsFactory.buyer_agent(context)
        else:
            raise ValueError(f"Invalid user type: {user_type}")
