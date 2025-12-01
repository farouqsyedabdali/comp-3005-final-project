import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import sys

DB_CONFIG = {
    'host': 'localhost',
    'database': 'fitness_club',
    'user': 'postgres',
    'password': 'Koolio@123'
}

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        print("\nPlease ensure:")
        print("1. PostgreSQL is running")
        print("2. Database 'fitness_club' exists")
        print("3. Password is set correctly in app/database.py")
        sys.exit(1)

def execute_query(query, params=None, fetch=True):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall() if fetch else None
            conn.commit()
            return result
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def execute_update(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def execute_transaction(queries_with_params):
    conn = get_connection()
    results = []
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            for query, params in queries_with_params:
                cursor.execute(query, params)
                if cursor.description:
                    results.append(cursor.fetchall())
                else:
                    results.append(cursor.rowcount)
            conn.commit()
            return results
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
