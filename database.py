import os
import psycopg2

DATABASE_URL = os.environ["DATABASE_URL"]

def connect():
    return psycopg2.connect(DATABASE_URL)