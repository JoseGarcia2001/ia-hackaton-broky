from abc import ABC, abstractmethod
from typing import Optional

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain.chat_models import init_chat_model

from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt.chat_agent_executor import AgentStateWithStructuredResponse

from pydantic import BaseModel, Field
from enum import Enum


class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"


class AgentResponse(BaseModel):
    type: MessageType = Field(description="Tipo de mensaje que se enviará al usuario:\n- text: Cuando va a enviar un mensaje de texto\n- image: Cuando va a enviar una imagen", default=MessageType.TEXT)
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
    def get_agents_description(self) -> str:
        """
        Get the description of the agents that will be used to process the user's message.

        Returns:
            str: The description of the agents that will be used to process the user's message.
        """
        pass

    def process(self) -> AgentResponse:
        """
        Processes the user's message

        Returns:
            str: The agent's response to the user's message.
        """
        agents: list[CompiledStateGraph] = self.get_agents()
        
        model = init_chat_model("openai:gpt-4.1", temperature=0)
        
        supervisor: StateGraph = create_supervisor(
            agents=agents,
            model=model,
            prompt=(
                "Eres un supervisor inteligente que gestiona los siguientes agentes especializados:\n"
                + self.get_agents_description()
                + "\n\nINSTRUCCIONES IMPORTANTES:\n"
                + "1. Analiza la solicitud del usuario y selecciona EXACTAMENTE UN agente apropiado\n"
                + "2. Delega completamente la tarea al agente seleccionado\n"
                + "3. NO respondas directamente al usuario, SIEMPRE deja que el agente responda\n"
                + "4. NO agregues comentarios adicionales a la respuesta del agente.\n"
                + "5. Usa emojis y caracteres especiales para hacer la respuesta más atractiva\n"
                + "6. La respuesta final DEBE ser únicamente el mensaje generado por el agente, el agente no tiene las herramientas para comunicarse con el usuario, eres tu quien debe comunicarte con el usuario\n"
                + "7. Si el agente no puede completar la tarea, permite que el agente informe esto al usuario\n\n"
                + "Tu único trabajo es seleccionar y transferir al agente correcto y retornar el mensaje de respuesta del agente al usuario"
            ),
            add_handoff_back_messages=True,
            output_mode="last_message",
            response_format=AgentResponse,
            state_schema=AgentStateWithStructuredResponse
        ).compile()

        # TODO: Implement the logic to retrieve messages from the database
        messages: list[BaseMessage] = [
            HumanMessage(content="Hola"),
        ]

        response = supervisor.invoke({"messages": messages}, {"run_name": self.__class__.__name__})

        message_response: AgentResponse = AgentResponse(
            type=MessageType.TEXT,
            message=response["messages"][-1].content
        )

        return message_response
