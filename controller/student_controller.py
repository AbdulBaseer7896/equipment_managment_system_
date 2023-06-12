from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash
from model.student_model import student_model
import datetime


obj = student_model()

def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator



@app.route('/student/profile' ,  methods=["GET", "POST"] )
@login_required('student')
def student_profile():
    print("This is student profile")
    
    data = request.args.get('data')
    result = str(data) 
    print("This is data of student profile " , data)
    result_dict = eval(result)
    profile_data = obj.take_student_profile_data(result_dict)
    # print("this is result " , result)
    # profile_data = obj.profile_data(result)
    if request.method == "GET":
    
        return render_template('student_URLs/student_profile.html' , data = data  , profile_data = profile_data )



@app.route('/student/book_equipment' ,  methods=["GET", "POST"] )
@login_required('student')
def book_equipment():
    data = request.args.get('data')
    result = str(data) 
    print("This is data of student profile " , data)
    data_new = eval(result)
    equipment_data = obj.take_equipment_data_form_db()
    # print("this is result " , result)
    # profile_data = obj.profile_data(result)
    path = request.args.get('data')
    print("The pate hsog jios  = " , data_new)
    if request.method == "GET":
        return render_template('student_URLs/book_equipment.html' , data = data  , equipment_data = equipment_data )
    if request.method == "POST":
        path = request.args.get('path')
        result = str(path) 
        path_new = eval(result)
        obj.stored_the_booking_information_in_bd(path_new , data_new)
        flash(("Your booking request is send to Sport Officer !!! Wait For Booking Approal !!!" , 'booking_request_send'))
        return render_template('student_URLs/student_dashboard.html' , data = data)





@app.route('/student/cheek_booking_aprovalment' ,  methods=["GET", "POST"] )
@login_required('student')
def cheek_booking_aprovalment():
    data = request.args.get('data')
    result = str(data) 
    data_new = eval(result)
    print("This is data of student profile " , data_new)
    
    booking_data = obj.take_student_booking_data_form_db(data_new)

    print("The pate hsog jios  = " , booking_data)
    if booking_data != []:
        if request.method == "GET":
            return render_template('student_URLs/cheek_booking_aproval.html' , data = data  , booking_data = booking_data )
    else:
        flash(("Sorry Sports Officer has not Approved your Booking!!! Kindly Wait untill Your Booking Will be Approved" , 'no_booking_approved'))
        return render_template('student_URLs/student_dashboard.html' , data = data)
    
    
    


@app.route('/student/cancel_booking' ,  methods=["GET", "POST"] )
@login_required('student')
def cancel_booking():
    data = request.args.get('data')
    result = str(data) 
    data_new = eval(result)
    print("This is data of student profile " , data_new)
    

    if request.method == "GET":
        booking_data = obj.take_student_cancle_booking_data_form_db(data_new)
        if booking_data != []:
            return render_template('student_URLs/cancel_booing.html' , data = data  , booking_data = booking_data )
        else:
            flash(("Sorry You have not Book any Equipmet!!! Kindly Book some Thing" , 'no_item_in_for_cancle'))
            return render_template('student_URLs/student_dashboard.html' , data = data)
    
    if request.method == "POST":
        print("This is post method")
        path = request.args.get('paths')
        data = request.args.get('data')
        print("This is isisis s is is " , path)
        result = str(path) 
        cancle_booking_data = eval(result)
        print("This data = = = " , cancle_booking_data)
        obj.delete_booking_from_db(cancle_booking_data)
        flash(("You Cancled your Booking succesfully !!!" , "cancled_booking"))
        return render_template('student_URLs/student_dashboard.html' , data = data )
