import os
import re
import sqlite3
import smtplib, ssl
from flask import session, flash
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

SECRETS = None
import json
with open('secrets.json') as json_file:
   SECRETS = json.load(json_file)

port = 465
admin = SECRETS['sender_email']
password = SECRETS['password']

def send_dfa_token(receiver):
    try:
        token = session['token']

        msg = EmailMessage()
        msg['Subject'] = 'DFA Token'
        msg['From'] = admin
        msg['To'] = receiver
        msg.set_content(f"""
        UWEC JOB FINDER
                        
        Token: {token}
        """)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(admin, password)
            output = server.send_message(msg)
            current_app.logger.info(f"\nAttempted to send email to {receiver}.\n Info: {output}")

    except Exception as e: 
        current_app.logger.error("Error: ", e)


def apply_for_job(job_id:int, with_transcript:bool, with_resume:bool):

    conn = get_db_conn()
    job_info = conn.execute(
        f"""SELECT user.id, user.email, job.title
            FROM user
            JOIN job ON user.id = job.user_id
        WHERE job.id = {job_id}"""
    ).fetchall()[0]

    try:
        msg = EmailMessage()
        msg["Subject"] = "Job Application"
        msg["From"] = admin
        msg["To"] = job_info['email'] # the email of the poster
        msg.set_content(
            f"""
            Hi,
            
            I am interested in the {job_info['title']} position that you've posted. 

            Thank you for considering me,

            {session['first_n']} {session['last_n']}            
            """
        )

        if with_transcript and session['transcript'] != None:
            with open(os.path.join(current_app.config['UPLOAD_FOLDER'], session['transcript']), 'rb') as t:
                file_data = t.read()
                msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=session['transcript'])

        if with_resume and session['resume'] != None:
            with open(os.path.join(current_app.config['UPLOAD_FOLDER'], session['resume']), 'rb') as r:
                file_data = r.read()
                msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=session['resume'])

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(admin, password)
            send_errors = server.send_message(msg)
            current_app.logger.info(f"\nAttempted to send email to {job_info['email']}.\n Info: {send_errors}")              

        # set the application in the database
        conn.execute(
            f"""INSERT INTO job_application
            (user_id, job_id)
            VALUES ({session['user_id']}, {job_id});"""
        )
        conn.commit()
        conn.close()

    except Exception as ex:
        current_app.logger.error("Error: ", ex)
        raise ex

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
    
def is_valid_password(password:str, repass=None) -> bool:

    if len(password) <= 5:
        flash('Password must have more than 5 characters!', category='error')
        return False

    

    if re.search('[^a-zA-Z]', password) == None:
        flash('Password must contain at least one non-alpha character!', category='error')
        return False

    
    if repass != None:
        if password != repass:
            flash('Passwords did NOT match!', category='error')
            return False
 
    
    return True
    