from app import app
from flask_login import UserMixin
from model.user_model import user_model
from flask import render_template , request, redirect, flash
import json
from functools import wraps
from flask import abort
from flask_login import current_user

obj = user_model()
import flask_login

from flask import Flask, render_template, redirect, url_for , request
from flask_login import LoginManager, login_required, current_user , login_user ,logout_user

from flask import session

app.secret_key = "your_secret_key_here"
# create a LoginManager object
login_manager = LoginManager(app)


# define a User class with required methods for Flask-Login
class User:
    def __init__(self, user_id):
        self.id = user_id
    def get_type(self):
        return self.type
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)


# This is most important function. 
# This function allow the user. And see which user login in web
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        flash(('This login page is just for School Student and School Staff. IF you are outsider then Kindly do not try to login !!!!', 'warning'))
        return render_template("login.html")
    
    elif request.method == 'POST':
        username = request.form['email_login']
        password = request.form['password_login']
        user_type = request.form['login-val']
        # if the request is a POST request, authenticate the user and redirect to the appropriate page
        data = request.form.to_dict()
        user_type = request.form.get('login-val')
        print(type(user_type))
        print("The user_type is = " , user_type)
        
        if obj.user_login_model(data):
            session['role'] = user_type
                        # Redirect to the appropriate dashboard based on the user's role
            if session['role'] == 'student':
                return redirect(url_for('student_dashboard' , data = data))
            elif session['role'] == 'sport_officer':
                print(data)
                return redirect(url_for('sport_officer_dashboard' , data = data))
            
            elif session['role'] == 'dispach_man':
                return redirect(url_for('dispach_man_dashboard' , data = data))
        else:
            print("NO match")
            flash(('Wrong email or password. Please try again.', 'fail_login'))
            return render_template("login.html")
    return render_template('login.html')


@app.route("/sign_up_for_student", methods=["GET", "POST"])
def sign_up_for_student():
        if request.method == "GET":
            return render_template("sign_up_for_student.html")
        if request.method == 'POST':
            data = request.form.to_dict()
            print("This data = = = " , data['student_email'])
            if obj.send_sign_up_data_to_db(data):
                flash(("You will Sign in Successfully !!! Kindly login Now !!!" , "sign_done"))
                return render_template('login.html')




# @app.route("/forget_password", methods=["GET", "POST"])
# def forget_password():
#         if request.method == "GET":
#         # if the request is a GET request, render the login form
#         # flash("Welcome to the website!", "success")
#             return render_template("Forget_password.html")
#         elif request.method == 'POST':
#             username = request.form['email_login']
#             password = request.form['password_login']
#             user_type = request.form['login-val']
#             data = request.form.to_dict()
            
#             if obj.forget_password(data):
#                 return render_template('login.html')
#             else:
#                 print("You email or user type is wrong")
#                 return render_template('forget_password.html')        
#         return render_template('login.html')

# # create a dashboard route and view function for student
@login_manager.user_loader
def load_user(user_id):
    return User(int(user_id))


@app.route('/logout')
def logout():
    # Remove the user's role from the session variable
    session.pop('role', None)

    # Redirect to the login page
    return redirect(url_for('login'))



# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect(url_for("login"))
