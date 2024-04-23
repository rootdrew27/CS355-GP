from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_session import Session
from flask import Blueprint
from JobFinder.helpers import get_db_conn, is_logged_in, send_dfa_token

auth = Blueprint('auth', __name__)

@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login(prev_page:str=None):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'] #encrypted password

        # query database to verify user
        conn = get_db_conn()
        result = conn.execute(
            f"""SELECT * FROM user 
            WHERE email='{email}' AND password='{password}"""
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

@auth.route('/logout', methods=['GET'])
def logout():
    session['email'].pop()
    return

@auth.route('/dfa', methods=['GET', 'POST'])
def dfa():

    if request.method == 'POST':
        token = request.form['token']

        if token == session['token']: # success
            
            conn = get_db_conn()
            result = conn.execute(f"""
            SELECT * from user WHERE email = {session['temp_email']};"""
            ).fetchall()

            session['first_n'] = result[0]['first_n']
            session['last_n'] = result[0]['last_n']
            session['email'] = result[0]['email']
            session['perm_lvl'] = result[0]['permission_level']
            
            return redirect(url_for('views.profile'))
    else:
        return render_template('dfa.html')
    