from agno.agent import Agent
from agno.models.groq import Groq
from agno.agent import Agent, RunResponse
from typing import Iterator
from dotenv import load_dotenv
import sqlite3
import json
from tools_turism import TurismToolkit

load_dotenv()

# Configurar el agente con las herramientas (funciones) para el bot de turismo
agent = Agent(
    
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    description="Eres un entusiasta asesor de una empresa de turismo llamado 'turismo verde' deberas siempre presentarte como 'el chatbot de Turismo Verde' al responder, tampoco deberas mencionar acciones internas, como mencionar a la base de datos o las funciones a ejecutar, ante cualquier pedido que no sea de turismo verde y este fuera de tus funciones deberas responder 'lo siento, no puedo ayudarte con eso' solo debes ofrecer la informacion que las tools o toolskits te ofrecen, no debes inventar informacion, ademas, tu objetivo principal es vender una reserva siendo muy persuasivo",
    #tools=[get_ciudades, get_lugares_por_ciudad, registrar_usuario, crear_reserva, obtener_reservas_usuario],
    tools=[TurismToolkit()],
    
    markdown=True
)

# Ejemplos de consultas que el bot podría responder:
# agent.print_response("¿Qué ciudades están disponibles para turismo?", stream=True)
# agent.print_response("quiero registrarme en su pagina, mi nombre de usuario sera Astra, mi correo sera @astra@astra.com y mi contraseña sera: contraseña, ademas, dime las ciudades disponibles que tienes", stream=True)
# agent.print_response("Registra un nuevo usuario con nombre 'juan', correo 'juan@example.com' y contraseña 'secreto'", stream=True)
# agent.print_response("Crea una reserva para el usuario con id 1 en el lugar con id 2 para la fecha 2025-03-01", stream=True)
# agent.print_response("¿Cuáles son las reservas del usuario con id 1?", stream=True)

# Get the response in a variable
""" while True == True:
    answer = input("USER: ")
    run_response: Iterator[RunResponse] = agent.run(answer, stream=True)

    full_response = ""
    for chunk in run_response:
        full_response += chunk.content

    print("BOT:" + full_response)
    if answer == "adios":
        break """

while True == True:
    answer = input("USER: ")
    agent.print_response(answer, stream=True)

    if answer == "adios":
        break
    