"""
Defines the PublisherAgent class, which is responsible for registering the available agenda of the seller and others
- Get the available agenda of the seller.
- Offer and creates a property details card*.
- Offer and get the appraisal of the property*.
- Offer to publish the property on the platforms*.
"""

from langsmith.schemas import Prompt
from app.core.agent.main import Agent

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent


class PublisherAgent(Agent):
    def get_agents(self) -> list[CompiledStateGraph]:
        agenda_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the agenda agent
            tools=[],
            prompt=Prompt(
                # TODO: Iterate over the prompt
                content="Eres un agente que se encarga de gestionar la agenda disponible del vendedor para programar visitas."
            )
        )
        
        property_card_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the property card agent
            tools=[],
            prompt=Prompt(
                # TODO: Iterate over the prompt
                content="Eres un agente que se encarga de crear fichas detalladas de propiedades con toda la información relevante."
            )
        )
        
        appraisal_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the appraisal agent
            tools=[],
            prompt=Prompt(
                # TODO: Iterate over the prompt
                content="Eres un agente que se encarga de realizar avalúos de propiedades basado en características del mercado."
            )
        )
        
        publishing_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the publishing agent
            tools=[],
            prompt=Prompt(
                # TODO: Iterate over the prompt
                content="Eres un agente que se encarga de publicar propiedades en diferentes plataformas digitales."
            )
        )
        
        qa_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the qa agent
            tools=[],
            prompt=Prompt(
                # TODO: Iterate over the prompt
                content="Eres un agente que se encarga de responder las dudas del usuario sobre gestión de agenda, fichas de propiedades, avalúos y publicación."
            )
        )
        
        return [agenda_agent, property_card_agent, appraisal_agent, publishing_agent, qa_agent]

    def get_agents_description(self) -> str:
        return (
            "- AgendaAgent: Agente especializado en gestionar la agenda disponible del vendedor para programar visitas.\n"
            "- PropertyCardAgent: Agente especializado en crear fichas detalladas de propiedades.\n"
            "- AppraisalAgent: Agente especializado en realizar avalúos de propiedades.\n"
            "- PublishingAgent: Agente especializado en publicar propiedades en plataformas digitales.\n"
            "- QAAgent: Agente especializado en responder dudas sobre gestión de propiedades y publicación."
        )