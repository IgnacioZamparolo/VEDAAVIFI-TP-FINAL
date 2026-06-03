import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "my_password",
    "database": "parrilla_argentina"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
