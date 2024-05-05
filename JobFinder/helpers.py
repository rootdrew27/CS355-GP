import sqlite3
import smtplib, ssl
from flask import session
from flask import current_app
from email.message import EmailMessage

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

# SECRETS = None
# import json
# with open('secrets.json') as json_file:
#    SECRETS = json.load(json_file)

# port = 465
# sender = SECRETS['sender_email']
# password = SECRETS['password']

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
            current_app.logger.info(f"\nAttempted to send email to {receiver}.\n Info: {output}")

    except Exception as e: 
        current_app.logger.error("Error: ", e)


def apply_for_job(user, job_id=None):

    conn = get_db_conn()
    r = conn.execute(
        f"""SELECT user.email
            FROM user
            JOIN job ON user.id = job.user_id
        WHERE job.id = {job_id}"""
    ).fetchall()[0]
    conn.close()

    

    try:
        msg = EmailMessage()
        msg["Subject"] = "Job Application"
        msg["From"] = sender
        msg["To"] = 

        with smtplib.SMTP("localhost") as server:
            server.send_message(msg)
        
    except Exception as ex:
        current_app.logger.error("Error: ", ex)

ALLOWED_EXTENSIONS = {'txt', 'pdf'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_email(email:str) -> bool:
    email_split = email.split('@')[-1].split('.')
    if email_split[-2] == 'uwec' and email_split[-1] == 'edu':
        return True
    else:
        return False    