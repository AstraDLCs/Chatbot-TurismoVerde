import json
import sqlite3
from agno.tools import Toolkit
from agno.utils.log import logger

class TurismToolkit(Toolkit):
    def __init__(self):
        # Cambiamos el nombre a "turism" y registramos las funciones.
        super().__init__(name="tools_turism")
        self.register(self.get_ciudades)
        self.register(self.get_lugares_por_ciudad)
        self.register(self.registrar_usuario)
        self.register(self.crear_reserva)
        self.register(self.obtener_reservas_usuario)

    def get_ciudades(self) -> str:
        """
        Retorna la lista de ciudades registradas en la base de datos en formato JSON.
        Se utiliza una consulta parametrizada (similar a PDO) para seguridad.
        """
        conn = None
        try:
            conn = sqlite3.connect("turismos.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, descripcion FROM Ciudades")
            rows = cursor.fetchall()
            ciudades = [
                {"id": row[0], "nombre": row[1], "descripcion": row[2]}
                for row in rows
            ]
            logger.info("Se obtuvieron las ciudades.")
            return json.dumps({"ciudades": ciudades})
        except sqlite3.Error as e:
            logger.error(f"Error al obtener ciudades: {e}")
            return json.dumps({"error": str(e)})
        finally:
            if conn:
                conn.close()

    def get_lugares_por_ciudad(self, ciudad_nombre: str) -> str:
        """
        Retorna la lista de lugares de una ciudad específica en formato JSON.
        Se une la tabla Lugares con Ciudades y se utiliza una consulta parametrizada.
        """
        conn = None
        try:
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
                {
                    "id": row[0],
                    "nombre": row[1],
                    "precio": row[2],
                    "moneda": row[3],
                    "descripcion": row[4],
                }
                for row in rows
            ]
            logger.info(f"Se obtuvieron lugares para la ciudad {ciudad_nombre}.")
            return json.dumps({"lugares": lugares})
        except sqlite3.Error as e:
            logger.error(f"Error al obtener lugares para {ciudad_nombre}: {e}")
            return json.dumps({"error": str(e)})
        finally:
            if conn:
                conn.close()

    def registrar_usuario(self, usuario: str, correo: str, contrasena: str) -> str:
        """
        Registra un nuevo usuario en la base de datos y retorna el resultado en formato JSON.
        Se utiliza una consulta parametrizada para evitar inyecciones SQL.
        """
        conn = None
        try:
            conn = sqlite3.connect("turismos.db")
            cursor = conn.cursor()
            query = "INSERT INTO Usuarios (usuario, correo, contrasena) VALUES (?, ?, ?)"
            cursor.execute(query, (usuario, correo, contrasena))
            conn.commit()
            logger.info(f"Usuario {usuario} registrado exitosamente.")
            return json.dumps({"mensaje": f"Usuario {usuario} registrado exitosamente."})
        except sqlite3.IntegrityError:
            logger.error("El usuario o correo ya existe.")
            return json.dumps({"error": "El usuario o correo ya existe."})
        except sqlite3.Error as e:
            logger.error(f"Error al registrar usuario {usuario}: {e}")
            return json.dumps({"error": str(e)})
        finally:
            if conn:
                conn.close()

    def crear_reserva(self, usuario_id: int, lugar_id: int, fecha_reserva: str) -> str:
        """
        Crea una reserva para un usuario en un lugar dado y retorna el resultado en formato JSON.
        Se utiliza una consulta parametrizada para mayor seguridad.
        """
        conn = None
        try:
            conn = sqlite3.connect("turismos.db")
            cursor = conn.cursor()
            query = "INSERT INTO Reservas (usuario_id, lugar_id, fecha_reserva) VALUES (?, ?, ?)"
            cursor.execute(query, (usuario_id, lugar_id, fecha_reserva))
            conn.commit()
            logger.info(f"Reserva creada para usuario {usuario_id} en lugar {lugar_id}.")
            return json.dumps({"mensaje": "Reserva creada exitosamente."})
        except sqlite3.Error as e:
            logger.error(f"Error al crear reserva para usuario {usuario_id}: {e}")
            return json.dumps({"error": str(e)})
        finally:
            if conn:
                conn.close()

    def obtener_reservas_usuario(self, usuario_id: int) -> str:
        """
        Retorna las reservas realizadas por un usuario en formato JSON.
        Se realiza una unión entre Reservas y Lugares para obtener información relevante.
        """
        conn = None
        try:
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
            reservas = [
                {"id": row[0], "lugar": row[1], "fecha_reserva": row[2]}
                for row in rows
            ]
            logger.info(f"Se obtuvieron reservas para el usuario {usuario_id}.")
            return json.dumps({"reservas": reservas})
        except sqlite3.Error as e:
            logger.error(f"Error al obtener reservas para el usuario {usuario_id}: {e}")
            return json.dumps({"error": str(e)})
        finally:
            if conn:
                conn.close()
