"""
Defines the RegisterAgent class, which is responsible for registering sellers in the database:
- Get the basic information of the seller and register it in the database.
- Get the basic information of the property and register it in the database.
- Request and process the images of the property.
- Generate the QR associated to the property.
"""

from src.app.core.agent.main import Agent
from src.app.core.tools.register import get_user_info, save_property_info, get_remaining_info

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent


class RegisterAgent(Agent):
    
    def get_agents(self) -> list[CompiledStateGraph]:

        property_registration_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the property registration agent
            tools=[save_property_info, get_user_info, get_remaining_info],
            # TODO: Iterate over the prompt
            prompt=(
                    "Eres un agente que se encarga de recopilar y registrar la información básica de la propiedad en la base de datos."
                    " Debes obtener del usuario los siguientes datos: \n"
                    "- Dirección de la propiedad\n"
                    "- Tipo de propiedad\n"
                    "- Precio de la propiedad\n"
                    "Usar la herramienta apropiada para registrar la información de la propiedad. Puedes realizar actualizaciones parciales de la información de la propiedad.\n"
                    "Recuerda saludar al usuario si es la primera vez que hablas con él e iniciar el proceso de registro."
            ),
            name="PropertyRegistrationAgent"
        )
        
        qr_generator_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the QR generator agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de generar el código QR asociado a la propiedad registrada.",
            name="QRGeneratorAgent"
        )
        
        qa_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the qa agent
            tools=[],
            # TODO: Iterate over the prompt
            prompt="Eres un agente que se encarga de responder las dudas del usuario sobre el proceso de registro de vendedores y propiedades.",
            name="QAAgent"
        )
        
        return [property_registration_agent, qr_generator_agent, qa_agent]

    def get_agents_description(self) -> str:
        return (
            "- PropertyRegistrationAgent: Agente especializado en el proceso de registro de la propiedad. Realiza y recopila la información necesaria de la propiedad\n"
            "- QRGeneratorAgent: Agente especializado en generar códigos QR asociados a las propiedades.\n"
            "- QAAgent: Agente especializado en responder dudas sobre el proceso de registro y la plataforma.\n"
            "NOTA: El proceso de registro debe siempre empezar con el PropertyRegistrationAgent."
        )