import psycopg2
import os
import dotenv



dotenv.load_dotenv()



DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_HOST = os.getenv("POSTGRES_HOST")

class PostgreSQLConnection:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn =  psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
                )
            print("Conexão com sucesso!")
        except psycopg2.Error as e:
            print("Erro ao conectar ao Postgre:", e)
