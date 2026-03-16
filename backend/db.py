import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()   #loads variables from .env file into Python

def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    conn = psycopg2.connect(database_url)

    return conn