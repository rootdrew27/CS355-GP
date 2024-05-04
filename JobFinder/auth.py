from flask import Flask, render_template, request, url_for, session, redirect, flash, current_app
#from flask_session import Session
from flask import Blueprint
from werkzeug.utils import secure_filename, send_from_directory
from JobFinder.helpers import get_db_conn, is_logged_in, send_dfa_token, allowed_file
import os



auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        resume = request.files['resume']
        transcript = request.files['transcript']

        # check to see if account exists with email
        conn = get_db_conn()
        r = conn.execute(
            f"""SELECT email FROM user WHERE email = '{email}';"""
        ).fetchall()
        if len(r) > 0:
            flash('An account already exists with this email!', category='error')
            return render_template('register.html')

        # check for valid input
        if fname and lname and password:
            email_split = email.split('@')[-1].split('.')
            if email_split[-2] == 'uwec' and email_split[-1] == 'edu':                 

                path_to_r_file = None
                path_to_t_file = None

                if resume and transcript:
                    if allowed_file(resume.filename) and allowed_file(transcript.filename):
                        r_filename = secure_filename(resume.filename)
                        t_filename = secure_filename(transcript.filename)

                        resume.save(os.path.join(current_app.config['UPLOAD_FOLDER'], r_filename))
                        transcript.save(os.path.join(current_app.config['UPLOAD_FOLDER'], t_filename))
                        path_to_r_file = current_app.config['UPLOAD_FOLDER'] + r_filename
                        path_to_t_file = current_app.config['UPLOAD_FOLDER'] + t_filename

                    elif allowed_file(resume.filename):
                        flash('Invalid Transcript', category='error')
                        return render_template('register.html')
                    elif allowed_file(transcript.filename):
                        flash('Invalid Resume', category='error')
                        return render_template('register.html')

                elif resume:
                    if allowed_file(resume.filename):
                        r_filename = secure_filename(resume.filename)
                        resume.save(os.path.join(current_app.config['UPLOAD_FOLDER'], r_filename))
                        path_to_r_file = current_app.config['UPLOAD_FOLDER'] + r_filename
                    else:            
                        flash('Invalid Resume!', category='error')
                        return render_template('register.html')

                elif transcript:
                    if allowed_file(transcript.filename):
                        t_filename = secure_filename(transcript.filename)
                        transcript.save(os.path.join(current_app.config['UPLOAD_FOLDER'], t_filename))
                        path_to_t_file = current_app.config['UPLOAD_FOLDER'] + t_filename
                    else:
                        flash('Invalid Transcript!', category='error')
                        return render_template('register.html')
                else:
                    pass

                conn = get_db_conn()
                conn.execute(
                    f"""INSERT INTO user (first_n, last_n, email, password, permission_level, path_to_r_file, path_to_t_file) VALUES ('{fname}', '{lname}', '{email}', '{password}', 1, '{path_to_r_file}', '{path_to_t_file}');"""
                    )
                conn.commit()
                conn.close()
                return render_template('login.html')

            else: 
                flash('Invalid Email', category='error')
                return render_template('register.html')
        else: 
            flash('Please enter a First name, Last name, and password ', category='error')
            return render_template('register.html')


    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'] #encrypted password

        # query database to verify user
        conn = get_db_conn()
        result = conn.execute(
            f"""SELECT * FROM user 
            WHERE email='{email}' AND password='{password}'"""
        ).fetchall()
        conn.close()

        if len(result) == 1:
            
            session['temp_email'] = email
            session['token'] = 'token' # TODO randomly generate this 

            send_dfa_token(email)
 
            flash(f'A DFA Token has been sent to {email}')
            return render_template('dfa.html')
        # start session

        else: # invalid credentials
            flash('Email or Password were invalid!', category='error')
            return render_template('login.html')

    # else, its a GET request
    return render_template('login.html')

@auth.route('/dfa', methods=['GET', 'POST'])
def dfa():

    if request.method == 'POST':
        token = request.form['token']

        if token == session['token']: # success
            
            conn = get_db_conn()
            result = conn.execute(f"""
            SELECT * from user WHERE email = '{session['temp_email']}';"""
            ).fetchall()

            session['first_n'] = result[0]['first_n']
            session['last_n'] = result[0]['last_n']
            session['email'] = result[0]['email']
            session['transcript'] = str(result[0]['path_to_t_file']).split('\\')[-1]
            session['resume'] = str(result[0]['path_to_r_file']).split('\\')[-1]
            session['perm_lvl'] = result[0]['permission_level']

            return redirect(url_for('views.student_profile'))
        else:
            flash('Invalid Token!', category='error')
            return render_template('dfa.html')
    else:
        return render_template('dfa.html')
    
@auth.route('/logout', methods=['GET'])
def logout():
    for e in [e for e in session]:
        session.pop(e, None)
    return redirect(url_for('auth.login'))

@auth.route('/forgot_password', methods=['GET'])
def forgot_password():
    pass

@auth.route('/upload_transcript', methods=['POST'])
def upload_transcript():
    try:

        transcript = request.files['transcript']

        email = session['email']

        if transcript:
            if allowed_file(transcript.filename):
                t_filename = secure_filename(transcript.filename)

                # delete old file (if it exists)
                conn = get_db_conn()
                r = conn.execute(
                    f"""SELECT path_to_t_file FROM user WHERE email = '{email}';"""
                ).fetchall()
                old_filename = r[0]['path_to_t_file']
                if old_filename:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], old_filename))

                transcript.save(os.path.join(current_app.config['UPLOAD_FOLDER'], t_filename))
                path_to_t_file = current_app.config['UPLOAD_FOLDER'] + t_filename

                # set the path_to_t_file
                conn.execute(
                    f"""UPDATE user SET path_to_t_file = '{path_to_t_file}' WHERE email = '{email}'"""
                )
                conn.commit()
                conn.close()

                session['transcript'] = t_filename

                flash('Transcript was Successfully Uploaded!')
                return redirect(url_for('views.student_profile'))

            else:
                flash('Invalid Transcript!', category='error')
                return redirect(url_for('views.student_profile'))
        else:
            flash('Invalid Transcript!', category='error')
            return redirect(url_for('views.student_profile'))
    except Exception as ex:
        flash('Error occurred while uploading transcript', category='error')
        return redirect(url_for('views.student_profile'))


@auth.route('/upload_resume', methods=['POST'])
def upload_resume():
    try:

        resume = request.files['resume']

        email = session['email']

        if resume:
            if allowed_file(resume.filename):
                r_filename = secure_filename(resume.filename)

                # delete old file (if it exists)
                conn = get_db_conn()
                r = conn.execute(
                    f"""SELECT path_to_t_file FROM user WHERE email = '{email}';"""
                ).fetchall()
                old_filename = r[0]['path_to_t_file']
                if old_filename:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], old_filename))

                resume.save(os.path.join(current_app.config['UPLOAD_FOLDER'], r_filename))
                path_to_t_file = current_app.config['UPLOAD_FOLDER'] + r_filename

                # set the path_to_t_file
                conn.execute(
                    f"""UPDATE user SET path_to_t_file = '{path_to_t_file}' WHERE email = '{email}'"""
                )
                conn.commit()
                conn.close()

                session['resume'] = r_filename

                flash('Resume was Successfully Uploaded!')
                return redirect(url_for('views.student_profile'))

            else:
                flash('Invalid Resume!', category='error')
                return redirect(url_for('views.student_profile'))
        else:
            flash('Invalid Resume!', category='error')
            return redirect(url_for('views.student_profile'))
    except Exception as ex:
        flash('Error occurred while uploading resume', category='error')
        return redirect(url_for('views.student_profile'))
