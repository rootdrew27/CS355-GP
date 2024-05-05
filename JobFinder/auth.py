from flask import Flask, render_template, request, url_for, session, redirect, flash, current_app
#from flask_session import Session
from flask import Blueprint
from werkzeug.utils import secure_filename, send_from_directory
from JobFinder.helpers import get_db_conn, is_logged_in, send_dfa_token, allowed_file, validate_email, is_valid_password
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
            if validate_email(email):             

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
            flash('Email and/or Password is invalid!', category='error')
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
            ).fetchall()[0]

            session['user_id'] = result['id']
            session['first_n'] = result['first_n']
            session['last_n'] = result['last_n']
            session['email'] = result['email']
            session['transcript'] = str(result['path_to_t_file']).split('\\')[-1]
            session['resume'] = str(result['path_to_r_file']).split('\\')[-1]
            session['perm_lvl'] = result['permission_level']
                

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
                if old_filename != 'None':
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
        current_app.logger.error("Error occurred while uploading a transcript.", ex)
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


@auth.route('update_email', methods=["POST"])
def update_email():
    
    email = request.form['email']
    old_email = session['email']

    if email == old_email:
        flash('This is the same email!', category='error')
        return redirect(url_for('views.student_profile'))

    conn = get_db_conn()

    if validate_email(email):

        conn.execute(f"""
            UPDATE user SET email = '{email}'
            WHERE email = '{old_email}';
        """)
        conn.commit()
        conn.close()

        session['email'] = email        

        flash('Email updated successfully!')
        return redirect(url_for('views.student_profile'))
    else:
        flash('Invalid Email!', category='error')
        return redirect(url_for('views.student_profile'))
    
@auth.route('update_password', methods=["POST"])
def update_password():
    
    password = request.form['password']
    rePass = request.form['rePassword']

    conn = get_db_conn()

    oldpassword = conn.execute(f"""SELECT password FROM user WHERE id = {session['user_id']}""").fetchall()[0]

    if oldpassword == password:
        flash('This was already your password!', category='info')
        return redirect(url_for('views.student_profile'))

    if (is_valid_password(password, rePass)) == False:
        return redirect(url_for('views.student_profile'))
    
    conn.execute(f"""
        UPDATE user
        SET password = '{password}' 
        WHERE id = {session['user_id']};
    """)
    conn.commit()
    conn.close()

    flash('Successfully updated password!')
    return redirect(url_for('views.student_profile'))
