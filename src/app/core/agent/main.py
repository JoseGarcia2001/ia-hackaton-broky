from abc import ABC, abstractmethod
from typing import Optional

from langchain import hub
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain.chat_models import init_chat_model

from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt.chat_agent_executor import AgentStateWithStructuredResponse

from pydantic import BaseModel, Field
from enum import Enum
from src.app.utils.logger import logger


class AgentState(AgentStateWithStructuredResponse):
    """
    The state of the agent.
    """
    chat_id: str = Field(description="ID del chat")


class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"


class AgentResponse(BaseModel):
    type: MessageType = Field(
        description="Tipo de mensaje que se enviará al usuario:\n- text: Cuando va a enviar un mensaje de texto\n- image: Cuando va a enviar una imagen",
        default=MessageType.TEXT,
    )
    message: Optional[str] = Field(description="Mensaje que se enviará al usuario o URL de la imagen", default=None)


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
    def get_flow_description(self) -> str:
        """
        Get the description of the flow that will be used to process the user's message.

        Returns:
            str: The description of the flow that will be used to process the user's message.
        """
        pass

    def process(self, agent_context: dict) -> AgentResponse:
        """
        Processes the user's message

        Args:
            agent_context: The context of the agent.

        Returns:
            str: The agent's response to the user's message.
        """
        logger.info(f"Processing agent {self.__class__.__name__}")
        agents: list[CompiledStateGraph] = self.get_agents()

        model = init_chat_model("openai:gpt-4.1", temperature=0)

        prompt = hub.pull("supervisor")
        prompt = prompt.format(flow_description=self.get_flow_description())

        supervisor: StateGraph = create_supervisor(
            agents=agents,
            model=model,
            prompt=prompt,
            add_handoff_back_messages=True,
            output_mode="last_message",
            response_format=AgentResponse,
            state_schema=AgentState,
        ).compile()

        messages: list[BaseMessage] = []
        for message in agent_context.get("conversation_history"):
            if message.get("sender") == "user":
                messages.append(HumanMessage(content=message.get("content")))
            elif message.get("sender") == "system":
                messages.append(AIMessage(content=message.get("content")))

        response = supervisor.invoke({"messages": messages, "chat_id": agent_context.get("chat_id")}, {"run_name": self.__class__.__name__, "metadata": {"chat_id": agent_context.get("chat_id")}})

        ai_messages = list(filter(lambda message: isinstance(message, AIMessage), response["messages"]))

        message_response: AgentResponse = AgentResponse(type=MessageType.TEXT, message=ai_messages[-2].content)

        return message_response
