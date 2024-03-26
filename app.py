"""test Flask with this"""

from flask import Flask, render_template, request, url_for, session, redirect
from flask_session import Session
import sqlite3
from markupsafe import escape
from datetime import timedelta
import json
import hashlib

app = Flask(__name__)

# app.config.from_file('./config.json', load=json.load)
# Session(app)
# app.config['SESSION_TYPE'] = 'memcached' # session info is stored via memcache api
# app.config['SESSION_PERMANENT'] = True # session are persisent, thus they are not ended when the brwoser closes
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60) # sessions lasts for 60 minutes unless renewed or explicitly cancelled.
# app.config['SESSION_REFRESH_EACH_REQUEST'] = True # session renew feature is enabled
app.secret_key = b'JF*FIWazxa3' 

######################## VIEWS #####################################

# home view
@app.route('/')
def index():
    x = True if 'email' in session else False
    app.logger.debug('Session is started ' + str(x))
    endpoint = url_for('job_finder')
    return render_template('index.html', endpoint=endpoint)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login(prev_page:str=None):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # password = hashlib.md5(request.form['password'].encode('utf-8'))

        # query database to verify user
        conn = get_db_conn()
        conn.execute(f"SELECT * FROM user WHERE email='{email}' AND password='{password}'")

        # start session
        session['email'] = email

        if prev_page == None:
            return redirect(url_for('index'))
        
        return redirect(url_for(prev_page))
        
    # else, its a GET request
    return render_template('login.html')

# job list view
@app.get('/jobs')
def job_finder():
    # get all jobs
    conn = get_db_conn()
    jobs = conn.execute('SELECT * FROM job').fetchall()
    conn.close()
    return render_template('jobs.html', jobs=jobs)

@app.get('/jobs/<int:job_id>')
def job_page():
    pass

@app.post('/jobs/<int:job_id>/apply')
def apply(job_id):
    # apply for the job (notify the poster and store info in db)
    # or redirect the client to the login page.
    pass

################## HELPER FUNCTIONS #################################
def get_db_conn():
    """Create a connection to the database

    Returns:
        Connection: an object which enables interfacing with the database
    """
    conn = sqlite3.connect('./db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

perm_lvls = {0: 'default', 1: 'student', 2: 'faculty'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)






