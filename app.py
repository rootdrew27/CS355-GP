"""test Flask with this"""

from flask import Flask, render_template, request, url_for, session
import sqlite3
from markupsafe import escape

app = Flask(__name__)

app.secret_key = b'JF*FIWazxa3'


######################## VIEWS #####################################

# home view
@app.route('/')
def home():
    return render_template("test.html", endpoint='test')

# test view
@app.route('/test')
def test():
    return f'success'

# job list view
@app.get('/jobs')
def job_finder():
    # get all jobs
    conn = get_db_conn()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return render_template('jobs.html', jobs=jobs)



################## HELPER FUNCTIONS #################################
def get_db_conn():
    """Create a connection to the database

    Returns:
        Connection: an object which enables interfacing with the database
    """
    conn = sqlite3.connect('./db/database.db')
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)


    # url for style sheet (use in templates)
    # url_for('static', filename='style.css')


