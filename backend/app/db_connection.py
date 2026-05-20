import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "my_password",
    "database": "parrilla_argentina"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
