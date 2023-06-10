from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash
from model.sport_officer_model import sport_officer_model
import datetime


obj = sport_officer_model()

def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator



@app.route('/sport_officer/add_equipments' ,  methods=["GET", "POST"] )
@login_required('sport_officer')
def add_new_equipments():
    print("This is student profile")
    data = request.args.get('data')
    if request.method == "GET":
        return render_template('sport_officer_URLs/add_new_equipments.html' , data = data )
    if request.method == "POST":
        new_equipments = request.form.to_dict()
        print("This data = = = " , new_equipments)
        image_file = request.files['image_of_product']
        if  image_file.filename != '':
            folder_name = 'images'
            image_path = obj.stored_image_in_file_and_send_path_in_db(image_file , folder_name)
        else:
            image_path = ""
        if obj.add_new_equipments_to_db(new_equipments , image_path):
            flash(("You Upload the new Equipment succesfully !!!" , "equipment_upload"))
        return render_template('sport_officer_URLs/sport_officer_dashboard.html' , data = data )



@app.route('/sport_officer/store' ,  methods=["GET", "POST"] )
@login_required('sport_officer')
def store():
    print("This is student profile")
    data = request.args.get('data')
    store_data = obj.take_store_data_from_db()
    if request.method == "GET":
        return render_template('sport_officer_URLs/store.html' , data = data , store_data = store_data )
    
    
    
 

@app.route('/sport_officer/approved_booding' ,  methods=["GET", "POST"] )
@login_required('sport_officer')
def approved_booding():
    data = request.args.get('data')
    booking_data = obj.take_booking_data_form_db()
    if request.method == "GET":
        return render_template('sport_officer_URLs/approved_booding.html' , data = data , booking_data = booking_data)
    if request.method == "POST":
        path = request.args.get('path')
        result = str(path) 
        cancle_booking_data = eval(result)
        print("This data = = = " , cancle_booking_data)
        obj.send_approved_booking_data_to_db(cancle_booking_data)
        flash(("You Approved the Booking succesfully !!!" , "approved_booking"))
        return render_template('sport_officer_URLs/sport_officer_dashboard.html' , data = data )
    


@app.route('/sport_officer/cancal_booking' ,  methods=["GET", "POST"] )
@login_required('sport_officer')
def cancal_booking():
    data = request.args.get('data')
    booking_data = obj.take_booking_approval_data_form_db()
    print("This booking data ==== " , booking_data)
    if booking_data != []:   
        if request.method == "GET":
            return render_template('sport_officer_URLs/cancal_booking.html' , data = data , booking_data = booking_data)
    else:
        flash(("Till Now you will not Approved any Booking !!!" , "you_not_approved_booking"))
        return render_template('sport_officer_URLs/sport_officer_dashboard.html' , data = data )
    
    if request.method == "POST":
        path = request.args.get('path')
        result = str(path) 
        cancle_booking_data = eval(result)
        print("This data = = = " , cancle_booking_data)
        obj.cancle_booking_data_from_db(cancle_booking_data)
        flash(("You Cancle the Booking succesfully !!!" , "cancle_booking"))
        return render_template('sport_officer_URLs/sport_officer_dashboard.html' , data = data )




