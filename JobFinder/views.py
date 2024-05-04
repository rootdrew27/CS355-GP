from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask import Blueprint
from .helpers import get_db_conn, is_logged_in

views = Blueprint('views', __name__)


perm_lvls = {0: 'default', 1: 'student', 2: 'faculty'}
######################## VIEWS #####################################
@views.route('/')
def home():
    x = is_logged_in()
    # logger.debug('Session is started: ' + str(x))
    return render_template('home.html', is_logged_in=is_logged_in(), session=session)

# job list view
@views.get('/jobs')
def job_finder():
    # get all jobs
    conn = get_db_conn()
    jobs = conn.execute(
        """SELECT job.id AS "job_id", job.title AS "job_title", job.date_listed, job.descrip AS "job_descrip", job.img_path, department.title AS "dept_title", user.first_n 
            FROM job 
            LEFT JOIN user ON job.user_id = user.id
            LEFT JOIN department ON job.dept_id = department.id;"""
    ).fetchall()
    conn.close()

    return render_template('jobs.html', jobs=jobs, is_logged_in=is_logged_in(), session=session)

@views.get('/jobs/<int:job_id>')
def get_job_info(job_id):
    conn = get_db_conn()
    job = conn.execute(f'SELECT * FROM job WHERE id = {job_id}').fetchall()
    conn.close()

    if job != None:
        job = job[0]
        return {
                'title': job['title'],
                'date_listed': job['date_listed'],
                'descrip': job['descrip']                
            } 



@views.route('/jobs/apply/<int:job_id>')
def apply(job_id):
    # apply for the job (notify the poster and store info in db)

    # or redirect the client to the login page.
 pass   
#    if session['email'] is not None:

@views.route('/student_profile')
def student_profile():
    if 'email' in session:
        return render_template('profile.html', session=session)
    else:
       flash("Login/Register to create your profile!", category='info')
       return redirect(url_for('auth.login'))

@views.route('/department')
def department():
    # get desired department
    conn = get_db_conn()
    jobs = conn.execute(
        """SELECT job.id AS "job_id", job.title AS "job_title", job.date_listed, job.descrip AS "job_descrip", job.img_path, department.title AS "dept_title", user.first_n 
            FROM job 
            LEFT JOIN user ON job.user_id = user.id
            LEFT JOIN department ON job.dept_id = department.id;"""
    ).fetchall()
    conn.close()
    return render_template('department.html')

@views.route('/department_profile/<int:dept_id>')
def department_profile():
    pass