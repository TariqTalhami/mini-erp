# Import PostgreSQL adapter for Python
# This library allows Python to connect and execute queries on a PostgreSQL database
import psycopg2

# Import os module to access environment variables
import os

# Import dotenv to load variables from a .env file (used in local development)
from dotenv import load_dotenv


# Load environment variables from .env file into the system environment
# This allows us to use os.getenv() to access them
load_dotenv()


# =========================
# DATABASE CONNECTION FUNCTION
# =========================
def get_db_connection():

    # Retrieve the database connection string from environment variables
    # Example format:
    # postgres://user:password@host:port/dbname
    database_url = os.getenv("DATABASE_URL")

    # If DATABASE_URL is not found, raise an error
    # This prevents the app from running without a valid database connection
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    # Establish connection to PostgreSQL database using the connection string
    conn = psycopg2.connect(database_url)

    # Return the connection object to be used in queries
    return conn