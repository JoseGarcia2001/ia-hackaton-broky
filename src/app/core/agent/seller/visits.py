"""
Defines the VisitsAgent which is responsible for managing the seller agenda
- Manage confirmation of the visits.
"""

from src.app.core.agent.main import Agent

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent


class VisitsAgent(Agent):
    def get_agents(self) -> list[CompiledStateGraph]:
        agenda_management_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the visit confirmation agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de gestionar la agenda del vendedor",
            name="AgendaManagementAgent"
        )
        
        qa_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the qa agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de responder las dudas del usuario sobre confirmación y gestión de visitas.",
            name="QAAgent"
        )

        property_card_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the property card agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de crear fichas detalladas de propiedades con toda la información relevante.",
            name="PropertyCardAgent"
        )
        
        appraisal_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the appraisal agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de realizar avalúos de propiedades basado en características del mercado.",
            name="AppraisalAgent"
        )
        
        publishing_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the publishing agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de publicar propiedades en diferentes plataformas digitales.",
            name="PublishingAgent"
        )
        
        return [agenda_management_agent, qa_agent, property_card_agent, appraisal_agent, publishing_agent]

    def get_flow_description(self) -> str:
        return (
            "- VisitConfirmationAgent: Agente especializado en confirmar, reprogramar o cancelar visitas de compradores\n"
            "- QAAgent: Agente especializado en responder dudas sobre gestión de visitas"
        )
