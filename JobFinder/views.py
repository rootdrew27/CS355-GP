from flask import Flask, render_template, request, url_for, session, redirect, flash, current_app, Response
import os
from flask import Blueprint
from .helpers import get_db_conn, is_logged_in, apply_for_job

views = Blueprint('views', __name__)


perm_lvls = {0: 'default', 1: 'student', 2: 'faculty'} # not in use

######################## VIEWS #####################################
@views.route('/')
def home():
    return render_template('home.html', session=session)

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

    if 'email' in session:
        jobsAppliedTo = conn.execute(f"""
            SELECT job_id FROM job_application WHERE user_id = {session['user_id']};
        """).fetchall()
        jobsAppliedTo = [job[0] for job in jobsAppliedTo]
    else: 
        jobsAppliedTo = ['']

    conn.close()

    return render_template('jobs.html', jobs=jobs, jobsAppliedTo=jobsAppliedTo, session=session)

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
    try:
        coverLetter = request.form['coverL']
        if 'transcript' in request.form:
            withTranscript = request.form['transcript']
        else:
            withTranscript = None

        if 'resume' in request.form:
            withResume = request.form['resume']
        else:
            withResume = None

        jobId = request.form['jobId']

        apply_for_job(jobId, withTranscript, withResume)

        flash("Successfully Applied!")
        return redirect(url_for('views.job_finder'))                                      
    except Exception as ex:
        current_app.logger.error(ex)
        flash("Failed to Apply", category='error')
        return redirect(url_for('views.job_finder'))
   

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
            LEFT JOIN department ON job.dept_id = department.id
            WHERE department.id = {dept_id};"""
    ).fetchall()  

    if 'email' in session:
        jobsAppliedTo = conn.execute(f"""
            SELECT job_id FROM job_application WHERE user_id = {session['user_id']};
        """).fetchall()
        jobsAppliedTo = [job[0] for job in jobsAppliedTo]
    else: 
        jobsAppliedTo = ['']

    dept_info = conn.execute(
        f"""SELECT id, title, email, descrip, website_url FROM department WHERE department.id = {dept_id};"""
    ).fetchall()[0]

    conn.close()
    return render_template('department.html', jobs=jobs, jobsAppliedTo=jobsAppliedTo, dept_info=dept_info)


@views.route('/manage_jobs')
def manage_jobs():

    conn = get_db_conn()
    jobs = conn.execute(f"""
        SELECT * from job WHERE user_id = {session['user_id']};
    """).fetchall()

    return render_template('manage_jobs.html', session=session, jobs=jobs)

@views.route('/create_job', methods=['POST'])
def create_job():
    title = request.form.get('title', None)
    descrip = request.form.get('descrip', None)
    image = request.files.get('image', None)

    if title != None and descrip != None and image != None:

        img_path = os.path.join(current_app.config['IMAGE_FOLDER'], image.filename)
        image.save(img_path)

        conn = get_db_conn()
        conn.execute(f"""
            INSERT INTO job (title, descrip, img_path, user_id) VALUES ('{title}', '{descrip}', '{img_path}', {session['user_id']});
        """)
        conn.commit()
        conn.close()
    else: 
        flash("Error entering job", category='error')
        return redirect(url_for('views.manage_jobs'))
    
    return redirect(url_for('views.manage_jobs'))

@views.route('/delete_job', methods=['POST'])
def delete_job():

    job_id = request.form.get('name', None)

    conn = get_db_conn()
    conn.execute(f"""
        DELETE FROM job WHERE id = {job_id};
    """)
    conn.commit()
    conn.close()

    return Response(status=204)