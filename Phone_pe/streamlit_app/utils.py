import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="tharun701",
        database="phonepe_data",
        port=3306
    )

def run_query(conn, query):
    return pd.read_sql(query, conn)