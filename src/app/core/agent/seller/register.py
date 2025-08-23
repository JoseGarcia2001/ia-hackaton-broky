"""
Defines the RegisterAgent class, which is responsible for registering sellers in the database:
- Get the basic information of the seller and register it in the database.
- Get the basic information of the property and register it in the database.
- Request and process the images of the property.
- Generate the QR associated to the property.
"""

from langsmith.schemas import Prompt
from app.core.agent.main import Agent

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent


class RegisterAgent(Agent):
    
    def get_agents(self) -> list[CompiledStateGraph]:
        seller_registration_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the seller registration agent
            tools=[],
            prompt=Prompt(
                # TODO: Iterate over the prompt
                content="Eres un agente que se encarga de recopilar y registrar la información básica del vendedor en la base de datos."
            )
        )
        
        property_registration_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the property registration agent
            tools=[],
            prompt=Prompt(
                # TODO: Iterate over the prompt
                content="Eres un agente que se encarga de recopilar y registrar la información básica de la propiedad en la base de datos."
            )
        )
        
        image_processing_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the image processing agent
            tools=[],
            prompt=Prompt(
                # TODO: Iterate over the prompt
                content="Eres un agente que se encarga de solicitar, recibir y procesar las imágenes de la propiedad."
            )
        )
        
        qr_generator_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the QR generator agent
            tools=[],
            prompt=Prompt(
                # TODO: Iterate over the prompt
                content="Eres un agente que se encarga de generar el código QR asociado a la propiedad registrada."
            )
        )
        
        qa_agent = create_react_agent(
            model="openai:gpt-4o",
            # TODO: Implement the tools for the qa agent
            tools=[],
            prompt=Prompt(
                # TODO: Iterate over the prompt
                content="Eres un agente que se encarga de responder las dudas del usuario sobre el proceso de registro de vendedores y propiedades."
            )
        )
        
        return [seller_registration_agent, property_registration_agent, image_processing_agent, qr_generator_agent, qa_agent]

    def get_agents_description(self) -> str:
        return (
            "- SellerRegistrationAgent: Agente especializado en registrar información básica de vendedores en la base de datos.\n"
            "- PropertyRegistrationAgent: Agente especializado en registrar información básica de propiedades en la base de datos.\n"
            "- ImageProcessingAgent: Agente especializado en solicitar y procesar imágenes de propiedades.\n"
            "- QRGeneratorAgent: Agente especializado en generar códigos QR asociados a las propiedades.\n"
            "- QAAgent: Agente especializado en responder dudas sobre el proceso de registro."
        )