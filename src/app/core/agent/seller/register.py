"""
Defines the RegisterAgent class, which is responsible for registering sellers in the database:
- Get the basic information of the seller and register it in the database.
- Get the basic information of the property and register it in the database.
- Request and process the images of the property.
- Generate the QR associated to the property.
"""

from src.app.core.agent.main import Agent
from src.app.core.tools.register import get_user_info, save_property_info, get_remaining_info, generate_qr

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from langchain import hub


class RegisterAgent(Agent):
    
    def get_agents(self) -> list[CompiledStateGraph]:
        prompt = hub.pull("property_registration_agent")

        property_registration_agent = create_react_agent(
            model="openai:gpt-4o",
            tools=[save_property_info, get_user_info, get_remaining_info, generate_qr],
            prompt=prompt.format(),
            name="PropertyRegistrationAgent"
        )
        
        return [property_registration_agent]

    def get_flow_description(self) -> str:
        return (
            "## FLUJO DE LA ETAPA DE REGISTRO\n"
            "Esta etapa sigue un flujo secuencial para completar el registro de propiedades:\n"
            "\n"
            "### Orden de Ejecución:\n"
            "1. **PropertyRegistrationAgent**: Recopila la información básica de la propiedad (dirección, tipo, precio) y genera el código QR asociado a la propiedad\n"
            "\n"
            "### Notas Importantes:\n"
            "- Cada agente debe completar su tarea antes de pasar al siguiente\n"
            "- Si hay errores en la recopilación de información, el PropertyRegistrationAgent debe resolverlos antes de continuar\n"
            "\n"
            "## AGENTES DISPONIBLES\n"
            "\n"
            "### 1. PropertyRegistrationAgent\n"
            "**Responsabilidades:**\n"
            "- Recopilar información básica de la propiedad (dirección, tipo, precio)\n"
            "- Registrar la información en la base de datos\n"
            "- Validar que toda la información requerida esté completa\n"
            "- Manejar actualizaciones parciales de la información\n"
        )