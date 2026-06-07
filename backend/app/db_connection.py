import mysql.connector
import os
from dotenv import load_dotenv

from constants import( 
DB_USER, 
DB_PASSWORD, 
DATABASE,
)

load_dotenv()


DB_CONFIG = {
    "host": "localhost",
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DATABASE
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
