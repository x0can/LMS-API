import sqlite3


def get_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect('_courses_.db')
    conn.row_factory = sqlite3.Row  # Access rows as dictionaries
    return conn
