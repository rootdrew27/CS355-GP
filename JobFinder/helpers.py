import sqlite3
import smtplib, ssl
from flask import session
from flask import current_app as app

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


SECRETS = None
import json
with open('secrets.json') as json_file:
    SECRETS = json.load(json_file)

port = 465
sender = SECRETS['sender_email']
password = SECRETS['password']

def send_dfa_token(receiver):
    try:
        token = session['token']

        message = f"""
        Subject: DFA TOKEN

        Token: {token}
        """

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender, password)
            output = server.sendmail(sender, receiver, message)
            app.logger.info(f"\nAttempted to send email to {receiver}.\n Info: {output}")

    except Exception as e: 
        app.logger.error("Error: ", e)



