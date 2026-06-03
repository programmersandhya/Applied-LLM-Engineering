import pyodbc
import pandas as pd
from logger_config import logger
import os
from dotenv import load_dotenv

load_dotenv(override=True)
SERVER = os.getenv('DB_SERVER')
DATABASE = os.getenv('DB_NAME')
def get_connection():
    try:
        logger.info("Initiating database connection.")
        connection = pyodbc.connect(
            f"""
            DRIVER={{ODBC Driver 17 for SQL Server}};
            SERVER={SERVER};
            DATABASE={DATABASE};
            Trusted_Connection=yes;
            """
        )
        return connection
    except Exception as e:
        logger.exception(f"get_connection : {str(e)}")
        return None



def execute_query(query):
    connection = None
    try:
        print("initiating db connection")
        connection = get_connection()
        if connection is None:
            logger.error("Database connection failed.")
            return None
        logger.info("Connection successful")
        logger.info(f"executing query:{query}")
        dataframe = pd.read_sql(query, connection)
        return dataframe

    except Exception as e:
        logger.exception(f"Database Error: {str(e)}")
        return None
    finally:
        if(connection):
            connection.close()
            logger.info("DB connection closed")

