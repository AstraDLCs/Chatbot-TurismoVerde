from agno.agent import Agent
from agno.models.groq import Groq
from agno.agent import Agent, RunResponse
from typing import Iterator
from dotenv import load_dotenv
import sqlite3
import json

load_dotenv()

def get_ciudades() -> str:
    """
    Retorna la lista de ciudades registradas en la base de datos en formato JSON.
    Se utiliza una consulta parametrizada (similar a PDO) para seguridad.
    """
    conn = sqlite3.connect("turismos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, descripcion FROM Ciudades")
    rows = cursor.fetchall()
    ciudades = [{"id": row[0], "nombre": row[1], "descripcion": row[2]} for row in rows]
    conn.close()
    return json.dumps({"ciudades": ciudades})

def get_lugares_por_ciudad(ciudad_nombre: str) -> str:
    """
    Retorna la lista de lugares de una ciudad específica en formato JSON.
    Se une la tabla Lugares con Ciudades y se utiliza una consulta parametrizada.
    """
    conn = sqlite3.connect("turismos.db")
    cursor = conn.cursor()
    query = """
        SELECT Lugares.id, Lugares.nombre, Lugares.precio, Lugares.moneda, Lugares.descripcion
        FROM Lugares
        INNER JOIN Ciudades ON Lugares.ciudad_id = Ciudades.id
        WHERE Ciudades.nombre = ?
    """
    cursor.execute(query, (ciudad_nombre,))
    rows = cursor.fetchall()
    lugares = [
        {"id": row[0], "nombre": row[1], "precio": row[2], "moneda": row[3], "descripcion": row[4]}
        for row in rows
    ]
    conn.close()
    return json.dumps({"lugares": lugares})

def registrar_usuario(usuario: str, correo: str, contrasena: str) -> str:
    """
    Registra un nuevo usuario en la base de datos y retorna el resultado en formato JSON.
    Se utiliza una consulta parametrizada para evitar inyecciones SQL.
    """
    try:
        conn = sqlite3.connect("turismos.db")
        cursor = conn.cursor()
        query = "INSERT INTO Usuarios (usuario, correo, contrasena) VALUES (?, ?, ?)"
        cursor.execute(query, (usuario, correo, contrasena))
        conn.commit()
        conn.close()
        return json.dumps({"mensaje": f"Usuario {usuario} registrado exitosamente."})
    except sqlite3.IntegrityError:
        return json.dumps({"error": "El usuario o correo ya existe."})

def crear_reserva(usuario_id: int, lugar_id: int, fecha_reserva: str) -> str:
    """
    Crea una reserva para un usuario en un lugar dado y retorna el resultado en formato JSON.
    Se utiliza una consulta parametrizada para mayor seguridad.
    """
    try:
        conn = sqlite3.connect("turismos.db")
        cursor = conn.cursor()
        query = "INSERT INTO Reservas (usuario_id, lugar_id, fecha_reserva) VALUES (?, ?, ?)"
        cursor.execute(query, (usuario_id, lugar_id, fecha_reserva))
        conn.commit()
        conn.close()
        return json.dumps({"mensaje": "Reserva creada exitosamente."})
    except sqlite3.Error as e:
        return json.dumps({"error": str(e)})

def obtener_reservas_usuario(usuario_id: int) -> str:
    """
    Retorna las reservas realizadas por un usuario en formato JSON.
    Se realiza una unión entre Reservas y Lugares para obtener información relevante.
    """
    conn = sqlite3.connect("turismos.db")
    cursor = conn.cursor()
    query = """
        SELECT Reservas.id, Lugares.nombre, Reservas.fecha_reserva
        FROM Reservas
        INNER JOIN Lugares ON Reservas.lugar_id = Lugares.id
        WHERE Reservas.usuario_id = ?
    """
    cursor.execute(query, (usuario_id,))
    rows = cursor.fetchall()
    reservas = [{"id": row[0], "lugar": row[1], "fecha_reserva": row[2]} for row in rows]
    conn.close()
    return json.dumps({"reservas": reservas})

# Configurar el agente con las herramientas (funciones) para el bot de turismo
agent = Agent(
    
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    description="Eres un entusiasta asesor de una empresa de turismo llamado 'turismo verde' deberas siempre presentarte como 'el chatbot de Turismo Verde' al responder, tampoco deberas mencionar acciones internas, como mencionar a la base de datos o las funciones a ejecutar, ante cualquier pedido que no sea de turismo verde y este fuera de tus funciones deberas responder 'lo siento, no puedo ayudarte con eso'",
    tools=[get_ciudades, get_lugares_por_ciudad, registrar_usuario, crear_reserva, obtener_reservas_usuario],
    markdown=True
)

# Ejemplos de consultas que el bot podría responder:
# agent.print_response("¿Qué ciudades están disponibles para turismo?", stream=True)
# agent.print_response("quiero registrarme en su pagina, mi nombre de usuario sera Astra, mi correo sera @astra@astra.com y mi contraseña sera: contraseña, ademas, dime las ciudades disponibles que tienes", stream=True)
# agent.print_response("Registra un nuevo usuario con nombre 'juan', correo 'juan@example.com' y contraseña 'secreto'", stream=True)
# agent.print_response("Crea una reserva para el usuario con id 1 en el lugar con id 2 para la fecha 2025-03-01", stream=True)
# agent.print_response("¿Cuáles son las reservas del usuario con id 1?", stream=True)

# Get the response in a variable
run_response: Iterator[RunResponse] = agent.run("dime oniichan", stream=True)

full_response = ""
for chunk in run_response:
    full_response += chunk.content

print(full_response)