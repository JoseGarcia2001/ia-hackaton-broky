"""
Defines the PublisherAgent class, which is responsible for registering the available agenda of the seller and others
- Get the available agenda of the seller.
- Offer and creates a property details card*.
- Offer and get the appraisal of the property*.
- Offer to publish the property on the platforms*.
"""

from src.app.core.agent.main import Agent, AgentState

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from langchain import hub

from src.app.core.tools.general import save_availability, update_business_stage
from src.app.models.business_stage import SellerStage


class PublisherAgent(Agent):
    def get_agents(self) -> list[CompiledStateGraph]:
        prompt = hub.pull("agenda_agent")
        agenda_agent = create_react_agent(
            model="openai:gpt-4.1",
            tools=[save_availability, update_business_stage],
            prompt=prompt.format(next_stage=SellerStage.VISITS.value),
            name="AgendaAgent",
            state_schema=AgentState
        )
        
        return [agenda_agent]

    def get_flow_description(self) -> str:
        return (
            "## FLUJO DE LA ETAPA DE PUBLICACIÓN\n"
            "Esta etapa sigue un flujo secuencial para completar la publicación de propiedades:\n"
            "\n"
            "### Orden de Ejecución:\n"
            "1. **AgendaAgent**: Gestiona la agenda disponible del vendedor para programar visitas.\n"
            "\n"
            "### Notas Importantes:\n"
            "- Cada agente debe completar su tarea antes de pasar al siguiente\n"
            "- Si hay errores en la recopilación de información, el AgendaAgent debe resolverlos antes de continuar\n"
            "\n"
            "## AGENTES DISPONIBLES\n"
            "\n"
            "### 1. AgendaAgent\n"
            "**Responsabilidades:**\n"
            "- Gestionar la agenda disponible del vendedor para programar visitas.\n"
            "- Almacenar el horario de disponibilidad del vendedor.\n"
        )