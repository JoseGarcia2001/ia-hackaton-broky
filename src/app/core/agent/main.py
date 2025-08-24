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

        # messages: list[BaseMessage] = []
        # for message in agent_context.get("conversation_history"):
        #     if message.get("sender") == "user":
        #         messages.append(HumanMessage(content=message.get("content")))
        #     elif message.get("sender") == "system":
        #         messages.append(AIMessage(content=message.get("content")))

        messages = [
            HumanMessage(content="Hola!"),
            AIMessage(content="Parece que necesitamos más información para completar el registro de tu inmueble. Necesito saber el tipo de propiedad que estás registrando (por ejemplo, apartamento, casa, local comercial, etc.). ¿Podrías proporcionarme esa información, por favor?"),
            HumanMessage(content="El tipo de propiedad es un apartamento"),
            AIMessage(content="¡Gracias por indicarme que tu propiedad es un apartamento! El tipo ha sido registrado correctamente.\n\nAhora, revisando la información, veo que aún necesitamos tu confirmación sobre la dirección. Tengo registrada la siguiente dirección: Calle 123 #45-67.\n\n¿Esta dirección es correcta para tu apartamento o necesitas que la actualicemos?"),
            HumanMessage(content="La dirección es correcta"),
            AIMessage(content="¡Perfecto! Tu apartamento ha sido registrado exitosamente con la siguiente información:\n\n- Tipo de propiedad: Apartamento\n- Dirección: Calle 123 #45-67\n- Precio: 350 millones de pesos\n\nTambién he generado el código QR único asociado a tu inmueble y actualizado la etapa de tu registro a “publicación”. \n\nComo siguiente paso, ¿podrías indicarme en qué días y horarios estarías disponible para atender visitas de interesados en tu propiedad? ¡Así podremos ayudarte a coordinar las citas de manera eficiente!"),
            HumanMessage(content="La verdad podría atender los sabados en la tarde"),
            AIMessage(content="¡Gracias por tu respuesta! Para poder agendar visitas de posibles compradores, ¿podrías indicarme un rango exacto de horas en los que estarías disponible los sábados en la tarde? Por ejemplo: de 2:00 p.m. a 6:00 p.m.\n\nEsto me permitirá organizar tu agenda de visitas de forma precisa. ¡Te agradezco mucho tu colaboración!"),
            HumanMessage(content="De 2 a 4"),
            AIMessage(content="¡Disponibilidad registrada exitosamente! Ahora tu agenda para atender visitas a tu apartamento es: sábados de 2:00 p.m. a 4:00 p.m.\n\nTe notificaremos cuando algún posible comprador agende una visita en este horario.\n\nAdemás, quiero ofrecerte algunos servicios adicionales que pueden ayudarte a vender más rápido tu inmueble:\n- Avalúo profesional de tu apartamento por solo 20,000 COP.\n- Publicación de tu inmueble en nuestros portales de venta por una suscripción mensual de 20,000 COP.\n- Ficha técnica completa por 20,000 COP, que incluye descripción, amenidades cercanas y avalúo.\n\n¿Te gustaría saber más sobre alguno de estos servicios?")
        ]

        response = supervisor.invoke({"messages": messages, "chat_id": agent_context.get("chat_id")}, {"run_name": self.__class__.__name__, "metadata": {"chat_id": agent_context.get("chat_id")}})

        message_response: AgentResponse = AgentResponse(type=MessageType.TEXT, message=response["messages"][-1].content)

        return message_response
