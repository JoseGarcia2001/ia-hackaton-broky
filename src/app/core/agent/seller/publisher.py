"""
Defines the PublisherAgent class, which is responsible for registering the available agenda of the seller and others
- Get the available agenda of the seller.
- Offer and creates a property details card*.
- Offer and get the appraisal of the property*.
- Offer to publish the property on the platforms*.
"""

from src.app.core.agent.main import Agent

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent


class PublisherAgent(Agent):
    def get_agents(self) -> list[CompiledStateGraph]:
        agenda_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the agenda agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de gestionar la agenda disponible del vendedor para programar visitas.",
            name="AgendaAgent"
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
        
        qa_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the qa agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de responder las dudas del usuario sobre gestión de agenda, fichas de propiedades, avalúos y publicación.",
            name="QAAgent"
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