import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector
import datetime


class student_model():
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


                
    def take_student_profile_data(self, data):
        print("The data os s = = = =", data['email_login'])
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * FROM student_information WHERE student_email = '{data['email_login']}';")
            result = conn.execute(query1).fetchall()
            print("Thus us user as you seee = " , result)
            print("it also works")
            if result:
                print("This is the result of take student:", result[0][0])
                return result
            else:
                return False
            
    def take_equipment_data_form_db(self ):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * FROM equipments;")
            result = conn.execute(query1).fetchall()
            print("Thus us user as you seee = " , result)
            print("it also works")
            if result:
                print("This is the result of take student:", result[0][0])
                return result
            else:
                return False
            
    def stored_the_booking_information_in_bd(self , path , data):
        print("The data os s = = = =", data['email_login'])
        print("The data os s = = = =", path)
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S, %A")
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * FROM equipmetns_booking where product_name = '{path[0]}' AND  product_type = '{path[3]}' AND student_email =  '{data['email_login']}';")
            result = conn.execute(query1).fetchall()
            if result:
                query2 = text(f"Update  equipmetns_booking  SET  number_of_products = (number_of_products + 1) ,  booking = '{formatted_datetime}'  WHERE product_name = '{path[0]}' AND product_type = '{path[3]}' ANd student_email = '{data['email_login']}';")
                conn.execute(query2)
                
            else:
                query2 = text(f"INSERT INTO equipmetns_booking VALUES ('{path[0]}', '{path[3]}' , '{data['email_login']}' ,'{formatted_datetime}' , 1 , '{path[5]}');")
                conn.execute(query2)
                print("its eassu")
            return True
        
        
    def take_student_booking_data_form_db(self , data):
        print("The data os s = = = =", data)
        print("The data os s = = = =", data['email_login'])
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * FROM equipmetns_booking_approved where  student_email =  '{data['email_login']}';")
            result = conn.execute(query1).fetchall()
            return result
        
    
        



