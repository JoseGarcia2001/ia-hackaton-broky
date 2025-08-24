"""
Defines the VisitsAgent which is responsible for managing the seller agenda
- Manage confirmation of the visits.
"""

from src.app.core.agent.main import Agent

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from langchain import hub

from src.app.core.tools.general import save_availability


class VisitsAgent(Agent):
    def get_agents(self) -> list[CompiledStateGraph]:
        prompt = hub.pull("agenda_agent")
        agenda_management_agent = create_react_agent(
            model="openai:gpt-4.1",
            # TODO: Implement the tools for the visit confirmation agent
            tools=[save_availability],
            # TODO: Iterate over the prompt
            prompt=prompt.format(),
            name="AgendaManagementAgent"
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
        
        return [agenda_management_agent, property_card_agent, appraisal_agent, publishing_agent]

    def get_flow_description(self) -> str:
        return (
            "## FLUJO DE LA ETAPA DE VISITAS\n"
            "Esta etapa sigue un flujo secuencial para completar la gestión de visitas:\n"
            "\n"
            "### Orden de Ejecución:\n"
            "1. **AgendaManagementAgent**: Gestiona la agenda del vendedor para programar visitas\n"
            "\n"
            "### Notas Importantes:\n"
            "- Cada agente debe completar su tarea antes de pasar al siguiente\n"
            "- Si hay errores en la recopilación de información, el AgendaManagementAgent debe resolverlos antes de continuar\n"
            "\n"
            "## AGENTES DISPONIBLES\n"
            "\n"
            "### 1. AgendaManagementAgent\n"
            "**Responsabilidades:**\n"
            "- Gestionar la agenda del vendedor para programar visitas\n"
            "- Almacenar el horario de disponibilidad del vendedor\n"
        )
