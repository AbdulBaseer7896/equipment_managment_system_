from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash



def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/student/dashboard' , methods=["GET", "POST"])
@login_required('student')
def student_dashboard():
    data = request.args.get('data')
    # Functionality for student dashboard
    flash(('Dear student to Welcome  to PAF-IAST SEIMS  !!! You Successfull Login !!!' , 'student_login'))
    return render_template("student_URLs/student_dashboard.html", data = data)

@app.route('/sport_officer/dashboard')
@login_required('sport_officer')
def sport_officer_dashboard():
    data = request.args.get('data')
    flash(('Dear Sport Officer Welcome to PAF-IAST SEIMS  !!! You Successfull Login !!!' , 'Sport_officer_login'))
    return render_template("Sport_officer_URLs/Sport_officer_dashboard.html" , data= data)

@app.route('/dispach_man/dashboard')
@login_required('dispach_man')
def dispach_man_dashboard():
    data = request.args.get('data')
    flash(('Dear Dispach Officer Welcome to PAF-IAST SEIMS !!! You Successfull Login !!!' , 'dispach_man_login'))
    return render_template('dispach_man_URLs/dispach_man_dashboard.html' , data = data)
