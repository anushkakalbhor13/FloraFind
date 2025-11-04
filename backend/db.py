# db.py
import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",       # your MySQL host
        user="root",            # your MySQL username
        password="anushka",# your MySQL password
        database="florafind"    # your DB name (use the one you created with schema.sql)
    )
    return connection
