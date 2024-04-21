import sqlite3
import os
from flask import session

################## HELPER FUNCTIONS #################################
def get_db_conn():
    """Create a connection to the database

    Returns:
        Connection: an object which enables interfacing with the database
    """
    conn = sqlite3.connect('./JobFinder/db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def is_logged_in() -> bool:
    return True if 'email' in session else False