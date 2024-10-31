import psycopg2
import dotenv
from src.core.config import settings


dotenv.load_dotenv()

class PostgreSQLConnection:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = settings.get_postgres_connection
            print("Conexão com sucesso!")
        except psycopg2.Error as e:
            print("Erro ao conectar ao Postgre:", e)
