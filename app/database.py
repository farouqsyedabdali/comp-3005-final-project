"""
Database connection module for Health and Fitness Club Management System
"""
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import sys

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'database': 'fitness_club',
    'user': 'postgres',
    'password': 'Koolio@123'
}

def get_connection():
    """
    Establish and return a database connection.
    Returns: psycopg2 connection object
    Raises: SystemExit if connection fails
    """
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
    """
    Execute a SELECT query and return results.
    
    Args:
        query: SQL query string
        params: Tuple of parameters for query
        fetch: Whether to fetch results (True for SELECT, False for INSERT/UPDATE/DELETE)
    
    Returns:
        List of dictionaries (rows) if fetch=True, None otherwise
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            conn.commit()
            return None
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def execute_update(query, params=None):
    """
    Execute an INSERT/UPDATE/DELETE query.
    
    Args:
        query: SQL query string
        params: Tuple of parameters for query
    
    Returns:
        Number of affected rows
    """
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
    """
    Execute multiple queries in a transaction.
    
    Args:
        queries_with_params: List of tuples (query, params)
    
    Returns:
        List of results from each query
    """
    conn = get_connection()
    results = []
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            for query, params in queries_with_params:
                cursor.execute(query, params)
                if cursor.description:  # Has results
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

