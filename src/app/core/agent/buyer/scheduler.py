"""
Defines the SchedulerAgent class, which is responsible for scheduling visits for the buyer.
- Get the available agenda of the seller and offer the best options to the buyer.
- Notify the seller about the visit.
- Manage cancellation/rescheduling of the visit.
"""

from src.app.core.agent.main import Agent

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent


class SchedulerAgent(Agent):
    def get_agents(self) -> list[CompiledStateGraph]:
        availability_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the availability agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de consultar la agenda disponible de vendedores y ofrecer las mejores opciones de horarios a compradores.",
            name="AvailabilityAgent"
        )
        
        booking_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the booking agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de programar visitas de compradores y notificar a los vendedores correspondientes.",
            name="BookingAgent"
        )
        
        management_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the management agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de gestionar cancelaciones y reprogramaciones de visitas desde la perspectiva del comprador.",
            name="ManagementAgent"
        )
        
        qa_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the qa agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de responder las dudas del comprador sobre programación y gestión de visitas a propiedades.",
            name="QAAgent"
        )
        
        return [availability_agent, booking_agent, management_agent, qa_agent]

    def get_flow_description(self) -> str:
        return (
            "- AvailabilityAgent: Agente especializado en consultar disponibilidad de horarios para visitas.\n"
            "- BookingAgent: Agente especializado en programar visitas y notificar a vendedores.\n"
            "- ManagementAgent: Agente especializado en cancelar o reprogramar visitas desde la perspectiva del comprador.\n"
            "- QAAgent: Agente especializado en responder dudas de compradores sobre programación de visitas."
        )
