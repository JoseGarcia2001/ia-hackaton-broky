from abc import ABC, abstractmethod

from langchain_core.messages import BaseMessage
from langgraph.prebuilt.chat_agent_executor import Prompt

from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph_supervisor import create_supervisor


class Agent(ABC):
    """
    Base class for all agents.
    """
    @abstractmethod
    def get_agents(self) -> list[CompiledStateGraph]:
        """
        Get the agents that will be used to process the user's message.

        Returns:
            list[CompiledStateGraph]: The agents that will be used to process the user's message.
        """
        pass

    @abstractmethod
    def get_agents_description(self) -> str:
        """
        Get the description of the agents that will be used to process the user's message.

        Returns:
            str: The description of the agents that will be used to process the user's message.
        """
        pass

    def process(self) -> str:
        """
        Processes the user's message

        Returns:
            str: The agent's response to the user's message.
        """
        agents: list[CompiledStateGraph] = self.get_agents()
        supervisor: StateGraph = create_supervisor(
            agents=agents,
            model="openai:gpt-4o",
            prompt=Prompt(
                content=(
                    "Eres un supervisor gestionando los siguientes agentes:\n"
                    + self.get_agents_description()
                    + "Elige al agente más adecuado para el trabajo a realizar. Asigna el trabajo a un agente a la vez, no asignes el mismo trabajo a varios agentes en paralelo. Tampoco hagas el trabajo tú, haz que un agente lo haga."
                )
            ),
            add_handoff_back_messages=True,
            output_mode="last_message",
        ).compile()

        # TODO: Implement the logic to retrieve messages from the database
        messages: list[BaseMessage] = []

        response = supervisor.invoke(
            messages=messages,
        )
        print(response)

        return response
