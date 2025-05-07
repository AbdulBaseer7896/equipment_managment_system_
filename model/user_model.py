import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
from flask import Flask


class user_model():
    engine = None

    def __init__(self):
        try:
            # db_connection = os.environ.get('pafiast_db_connection')
            # self.engine = create_engine("mysql+pymysql://root@127.0.0.1:3306/Paf_Iast_EMS")

            # self.engine = create_engine(db_connection, connect_args={
            #     "ssl": {
            #         "ssl_ca": "/etc/ssl/cert.pem"
            #     }
            # })
            self.engine = create_engine("mysql+pymysql://root@127.0.0.1:3306/Paf_Iast_EMS")
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
        
    


    def send_sign_up_data_to_db(self, data):
        if not self.engine:
            print("No database connection!")
            return False

        try:
            with self.engine.begin() as conn:  # Use begin() for transactions
                # Check existing user
                check_query = text("""
                    SELECT * FROM student_information 
                    WHERE student_email = :email OR B_form_number = :bform
                """)
                user = conn.execute(check_query, {
                    'email': data['student_email'],
                    'bform': data['B_form_number']
                }).fetchall()

                if user:
                    flash(("Email/CNIC already exists!", "same_id_or_cnic_number"))
                    return render_template("sign_up_for_student.html")
                
                # Insert student information
                insert_student = text("""
                    INSERT INTO student_information VALUES (
                        :name, :bform, :email, :password, 
                        :religion, :gender, :dept, :dob, 
                        :guardian, :whatsapp, :program, 
                        :blood, :sport, :address
                    )
                """)
                conn.execute(insert_student, {
                    'name': data['student_name'],
                    'bform': data['B_form_number'],
                    'email': data['student_email'],
                    'password': data['student_password'],
                    'religion': data['student_religion'],
                    'gender': data['student_gender'],
                    'dept': data['student_department'],
                    'dob': data['student_dob'],
                    'guardian': '',  # Assuming guardian_contact column exists
                    'whatsapp': data['whatsApp_number'],
                    'program': data['student_program'],
                    'blood': data['student_blood'],
                    'sport': data['favourit_sport'],
                    'address': data['student_address']
                })

                # Insert into user_login
                insert_login = text("""
                    INSERT INTO user_login VALUES (
                        :email, :password, 'student'
                    )
                """)
                conn.execute(insert_login, {
                    'email': data['student_email'],
                    'password': data['student_password']
                })
                
                return True
            
        except Exception as e:
            print(f"Database error: {str(e)}")
            return False
        



    def changed_password_from_db(self , data):
        print("This i s data dat a = = " , data)
        print(data['email_login'])
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM user_login WHERE user_name = '{data['email_login']}' AND password = '{data['old_password_login']}'  AND  user_type = 'student';")
            user = conn.execute(query).fetchall()
            print("its work")
            
            if user:
                query1 = text(f"UPDATE user_login SET password = '{data['new_password_login']}' WHERE user_name ='{data['email_login']}'  AND user_type = 'student';")
                conn.execute(query1)
                print("its also work")
                return True
            else:
                print("its also work bad")
                return False
        
