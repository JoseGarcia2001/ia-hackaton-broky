"""
Defines the VisitsAgent which is responsible for managing the seller agenda
- Manage confirmation of the visits.
"""

from src.app.core.agent.main import Agent

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent


class VisitsAgent(Agent):
    def get_agents(self) -> list[CompiledStateGraph]:
        visit_confirmation_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the visit confirmation agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de confirmar, reprogramar o cancelar visitas de compradores a propiedades desde la perspectiva del vendedor.",
            name="VisitConfirmationAgent"
        )
        
        qa_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the qa agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de responder las dudas del usuario sobre confirmación y gestión de visitas.",
            name="QAAgent"
        )
        
        return [visit_confirmation_agent, qa_agent]

    def get_agents_description(self) -> str:
        return (
            "- VisitConfirmationAgent: Agente especializado en confirmar, reprogramar o cancelar visitas de compradores\n"
            "- QAAgent: Agente especializado en responder dudas sobre gestión de visitas"
        )
