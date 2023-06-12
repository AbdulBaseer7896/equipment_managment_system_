import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector


class user_model():
    engine = None

    def __init__(self):
        try:
            db_connection = os.environ.get('pafiast_db_connection')
            print(f"db_connection: {db_connection}")
            self.engine = create_engine(db_connection, connect_args={
                "ssl": {
                    "ssl_ca": "/etc/ssl/cert.pem"
                }
            })
            print("connection build successfully")
        except:
            print("not work")


    def user_login_model(self, data):
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM user_login WHERE user_name = '{data['email_login']}' AND password = '{data['password_login']}' AND user_type = '{data['login-val']}';")
            user = conn.execute(query).fetchall()
        if user:
            print(data['login-val'])
            return True
        else:
            print(data['login-val'])
            return False
        
        
    def send_sign_up_data_to_db(self , data):
        print("This is send sign up data to bd")
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * FROM student_information WHERE student_email = '{data['student_email']}' or B_form_number = '{data['B_form_number']}';")
            user = conn.execute(query1).fetchall()
            print("Thus us user as you seee = " , user)
            if user:
                print("no this is work 00 ")
                flash(("You Email or CNIC Number Is already Used !!! Kinldy used any other email or CNIC Number !!!" , "same_id_or_cnic_number"))
                return render_template("sign_up_for_student.html")
            else:
                print("Now this will else")
                query2 = text(f"INSERT INTO student_information VALUES ('{data['student_name']}', '{data['B_form_number']}', '{data['student_email']}', '{data['student_password']}', '{data['student_religion']}', '{data['student_gender']}', '{data['student_department']}', '{data['student_dob']}', '', '{data['whatsApp_number']}', '{data['student_program']}', '{data['student_blood']}', '{data['favourit_sport']}', '{data['student_address']}');")
                conn.execute(query2)
                print("This ins true as you see ")
                
                query3 = text(f"INSERT INTO user_login VALUES ('{data['student_email']}', '{data['student_password']}', 'student');")
                conn.execute(query3)
                return True
        
    # def forget_password(self , data):
    #     with self.engine.connect() as conn:
    #         query = text(f"SELECT * FROM user_login_table WHERE user_name = '{data['email_login']}'  AND user_type = '{data['login-val']}';")
    #         user = conn.execute(query).fetchall()
            
    #         query1 = text(f"UPDATE user_login_table SET password = '{data['password_login']}' WHERE user_name ='{data['email_login']}'  AND user_type = '{data['login-val']}';")
    #         user = conn.execute(query1)
    #     if user:
    #         print(data['login-val'])
    #         return True
    #     else:
    #         print(data['login-val'])
    #         return False
        