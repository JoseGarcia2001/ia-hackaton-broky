"""
Defines the SchedulerAgent class, which is responsible for scheduling visits for the buyer.
- Get the available agenda of the seller and offer the best options to the buyer.
- Notify the seller about the visit.
- Manage cancellation/rescheduling of the visit.
"""

from datetime import datetime

from src.app.core.agent.main import Agent

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from langchain import hub

from src.app.core.tools.buyer.scheduler import (
    save_buyer_info,
    get_seller_availability,
    save_visit_info,
    notify_seller,
    get_remaining_buyer_info,
)


class SchedulerAgent(Agent):
    def get_agents(self) -> list[CompiledStateGraph]:
        prompt = hub.pull("booking_agent")

        booking_agent = create_react_agent(
            model="openai:gpt-4.1",
            tools=[
                get_remaining_buyer_info,
                save_buyer_info,
                get_seller_availability,
                save_visit_info,
                notify_seller,
            ],
            prompt=prompt.format(current_date=datetime.now().strftime("%Y-%m-%d")),
            name="BookingAgent",
        )

        return [booking_agent]

    def get_flow_description(self) -> str:
        return (
            "## FLUJO DE LA ETAPA DE PROGRAMACIÓN DE VISITAS\n"
            "Esta etapa sigue un flujo secuencial para completar la programación de visitas:\n"
            "\n"
            "### Orden de Ejecución:\n"
            "1. **BookingAgent**: Programa visitas de compradores y notifica a los vendedores correspondientes\n"
            "\n"
            "### Notas Importantes:\n"
            "- Cada agente debe completar su tarea antes de pasar al siguiente\n"
            "- Si hay errores en la recopilación de información, el BookingAgent debe resolverlos antes de continuar\n"
            "\n"
            "## AGENTES DISPONIBLES\n"
            "\n"
            "### 1. BookingAgent\n"
            "**Responsabilidades:**\n"
            "- Registrar al comprador en la base de datos\n"
            "- Programar visitas de compradores y notificar a los vendedores correspondientes\n"
        )
