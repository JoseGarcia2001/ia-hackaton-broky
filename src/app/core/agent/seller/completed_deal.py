"""
Defines the CompletedDealAgent which handles the final stage after a successful property visit
- Generate sales contracts (contrato de compra y venta)
- Manage legal documentation and requirements
- Schedule contract signing appointments
- Track payment status and finalize property transfers
"""

from src.app.core.agent.main import Agent, AgentState
from src.app.core.tools.contracts import (
    generate_sales_contract, 
)
from src.app.core.tools.general import update_business_stage

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from langchain import hub


class CompletedDealAgent(Agent):
    def get_agents(self) -> list[CompiledStateGraph]:
        # Contract management agent for handling the completed deal flow
        contract_agent = create_react_agent(
            model="openai:gpt-4o",
            tools=[generate_sales_contract],
            prompt=(
                "Eres un agente especializado en la gestión de acuerdos completados de compra y venta de propiedades. "
                "Tu función es seguir un flujo conversacional específico con los vendedores.\n\n"
                "**FLUJO OBLIGATORIO:**\n"
                "1. **PRIMER MENSAJE**: Usa get_last_buyer_from_visit para obtener el nombre del comprador y pregunta: "
                "'¡Hola! ¿Cómo te fue con tu visita con [nombre del comprador]?'\n"
                "2. **ESPERAR RESPUESTA**: El vendedor te contará cómo fue la visita\n"
                "3. **SI DICE QUE SE CONCRETÓ LA VENTA**: Pregunta '¿Te gustaría que genere el contrato de compra y venta?'\n"
                "4. **SOLO SI CONFIRMA QUE SÍ**: Entonces usa generate_sales_contract\n\n"
                "**REGLAS IMPORTANTES:**\n"
                "- NUNCA generes el contrato hasta que el usuario confirme que quiere el contrato\n"
                "- SIEMPRE empieza preguntando sobre la visita con el comprador\n"
                "- Mantén un tono amigable y conversacional\n"
                "- Si no hay información del comprador, usa 'comprador' como fallback\n"
                "- NO hagas múltiples acciones en un solo mensaje, sigue el flujo paso a paso"
            ),
            name="ContractManagementAgent",
            state_schema=AgentState
        )

        return [contract_agent]
        
    def get_flow_description(self) -> str:
        return (
            "## FLUJO DE LA ETAPA DE ACUERDO COMPLETADO\n"
            "Esta etapa se activa cuando el vendedor reporta sobre el resultado de una visita "
            "y sigue un flujo conversacional estructurado.\n"
            "\n"
            "### Flujo Conversacional:\n"
            "1. **Pregunta inicial**: '¿Cómo te fue con tu visita con [nombre del comprador]?'\n"
            "2. **Evaluación de respuesta**: El agente escucha si la visita resultó exitosa\n"
            "3. **Oferta de contrato**: Si hubo acuerdo, pregunta si quiere el contrato\n"
            "4. **Generación**: Solo genera contrato si el vendedor confirma que sí\n"
            "\n"
            "### Orden de Ejecución:\n"
            "1. **ContractManagementAgent**: Maneja todo el flujo conversacional\n"
            "\n"
            "### Notas Importantes:\n"
            "- El proceso SIEMPRE inicia preguntando sobre la visita\n"
            "- No genera contratos automáticamente, requiere confirmación\n"
            "- Sigue un flujo paso a paso, sin hacer múltiples acciones\n"
            "\n"
            "## AGENTES DISPONIBLES\n"
            "\n"
            "### 1. ContractManagementAgent\n"
            "**Responsabilidades:**\n"
            "- Preguntar sobre el resultado de la visita\n"
            "- Ofrecer generación de contrato solo si hubo acuerdo\n"
            "- Generar contratos de compra y venta bajo confirmación\n"
            "\n"
            "### Frases que Activan esta Etapa:\n"
            "- 'Se cerró el trato'\n"
            "- 'Hubo acuerdo después de la visita'\n"
            "- 'El comprador está interesado en comprar'\n"
            "- 'Vamos a proceder con la venta'\n"
            "- 'Ya tuve la visita con el comprador'"
        )
