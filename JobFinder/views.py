from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask import Blueprint
from .helpers import get_db_conn, is_logged_in, apply_for_job

views = Blueprint('views', __name__)


perm_lvls = {0: 'default', 1: 'student', 2: 'faculty'}
######################## VIEWS #####################################
@views.route('/')
def home():
    return render_template('home.html', is_logged_in=is_logged_in(), session=session)

# job list view
@views.get('/jobs')
def job_finder():
    # get all jobs
    conn = get_db_conn()
    jobs = conn.execute(
        """SELECT job.id AS "job_id", job.title AS "job_title", job.date_listed, job.descrip AS "job_descrip", job.img_path, department.title AS "dept_title", user.first_n AS "first_n", user.last_n AS "last_n", job.dept_id AS 'dept_id' 
            FROM job 
            LEFT JOIN user ON job.user_id = user.id
            LEFT JOIN department ON job.dept_id = department.id;"""
    ).fetchall()
    conn.close()

    return render_template('jobs.html', jobs=jobs, is_logged_in=is_logged_in(), session=session)

@views.get('/jobs/<int:job_id>')
def get_job_info(job_id):
    conn = get_db_conn()
    job = conn.execute(
        f"""SELECT job.id AS "job_id", job.title AS "job_title", job.date_listed, job.descrip AS "job_descrip", job.img_path, department.title AS "dept_title", user.first_n AS "first_n", user.last_n AS "last_n" 
            FROM job 
            LEFT JOIN user ON job.user_id = user.id
            LEFT JOIN department ON job.dept_id = department.id
        WHERE job.id = {job_id};"""
    ).fetchall()[0]
    conn.close()

    if job != None:        
        return {
                'job_id': job['job_id'],
                'title': job['job_title'],
                'date_listed': job['date_listed'],
                'descrip': job['job_descrip'],
                'first_n': job['first_n'],
                'last_n': job['last_n'],
                'dept_title': job['dept_title']     
            } 


@views.route('/apply', methods=['POST'])
def apply():

    apply_for_job()                                         

    

@views.route('/student_profile')
def student_profile():
    if 'email' in session:
        return render_template('profile.html', session=session)
    else:
       flash("Login/Register to create your profile!", category='info')
       return redirect(url_for('auth.login'))

@views.route('/departments')
def departments():
    pass

@views.route('/department_profile/<int:dept_id>')
def department_profile(dept_id):
    # get desired department
    conn = get_db_conn()
    jobs = conn.execute(
        f"""SELECT job.id AS id, job.title AS title, job.date_listed, job.descrip, job.img_path, user.first_n, user.last_n 
            FROM job 
            LEFT JOIN user ON job.user_id = user.id
            JOIN department ON job.dept_id = {dept_id};"""
    ).fetchall()  

    dept_info = conn.execute(
        f"""SELECT id, title, email, descrip FROM department WHERE department.id = {dept_id};"""
    ).fetchall()[0]

    conn.close()
    return render_template('department.html', jobs=jobs, dept_info=dept_info)