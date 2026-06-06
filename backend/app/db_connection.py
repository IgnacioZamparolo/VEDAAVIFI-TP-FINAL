import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


DB_CONFIG = {
    "host": "localhost",
    "user": "admin",
    "password": "1234",
    "database": "parrilla_argentina"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
