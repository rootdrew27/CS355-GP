from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_session import Session
from flask import Blueprint
from JobFinder.helpers import get_db_conn, is_logged_in

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
            f"""SELECT first_n FROM user 
            WHERE email='{email}' AND password='{password}"""
        ).fetchall()
        conn.close()

        if len(result) == 1:
            # start session
            session['email'] = email
            session['first_n'] = result[0][0]

        else: # invalid credentials
            flash('Email or Password were invalid!', category='error')
            return

        if prev_page == None:
            return redirect(url_for('index'))
        
        return redirect(url_for(prev_page))
        
    # else, its a GET request
    return render_template('login.html')

@auth.route('/logout', methods=['GET'])
def logout():
    session['email'].pop()
    return