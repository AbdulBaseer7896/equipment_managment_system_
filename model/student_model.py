import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import datetime


class student_model():
    engine = None

    def __init__(self):
        try:
            # db_connection = os.environ.get('pafiast_db_connection') 
            # print(f"db_connection: {db_connection}")
            # self.engine = create_engine(db_connection, connect_args={
            #     "ssl": {
            #         "ssl_ca": "/etc/ssl/cert.pem"
            #     }
            # })
            self.engine = create_engine("mysql+pymysql://root@127.0.0.1:3306/Paf_Iast_EMS")

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
            


    def stored_the_booking_information_in_bd(self, path, data):
        print("Student email:", data['email_login'])
        print("Path data:", path)
        
        try:
            # Verify path structure
            if len(path) < 6:
                raise ValueError("Invalid path parameter structure")

            with self.engine.begin() as conn:  # Use transaction
                # 1. Check existing booking
                check_query = text("""
                    SELECT * FROM equipments_booking 
                    WHERE product_name = :name 
                    AND product_type = :type 
                    AND student_email = :email
                """)
                result = conn.execute(check_query, {
                    'name': path[0],
                    'type': path[3],
                    'email': data['email_login']
                }).fetchall()

                # 2. Use proper datetime format
                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if result:
                    # Update existing booking
                    update_query = text("""
                        UPDATE equipments_booking 
                        SET number_of_products = number_of_products + 1,
                            booking = :datetime
                        WHERE product_name = :name 
                        AND product_type = :type 
                        AND student_email = :email
                    """)
                    conn.execute(update_query, {
                        'datetime': current_datetime,
                        'name': path[0],
                        'type': path[3],
                        'email': data['email_login']
                    })
                else:
                    # Insert new booking
                    insert_query = text("""
                        INSERT INTO equipments_booking 
                        (product_name, product_type, student_email, 
                        booking, number_of_products, image_path)
                        VALUES (:name, :type, :email, :time, 1, :img)
                    """)
                    conn.execute(insert_query, {
                        'name': path[0],
                        'type': path[3],
                        'email': data['email_login'],
                        'time': current_datetime,
                        'img': path[5]
                    })

                print("Booking processed successfully")
                return True

        except Exception as e:
            print(f"Database operation failed: {str(e)}")
            return False

        
    def take_student_booking_data_form_db(self , data):
        print("The data os s = = = =", data)
        print("The data os s = = = =", data['email_login'])
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * FROM equipments_booking_approved where  student_email =  '{data['email_login']}';")
            result = conn.execute(query1).fetchall()
            return result
        
        
        
    def take_student_cancle_booking_data_form_db(self , data):
        print("THis jii isdj 33     333333 = " , data)
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * From equipments_booking where student_email = '{data['email_login']}';")
            cheek = conn.execute(query1).fetchall()
            return cheek
        

    # def take_student_cancle_booking_data_form_db(self, data):
    #     print("Fetching booking data for:", data['email_login'])
    #     try:
    #         with self.engine.connect() as conn:
    #             # Use parameterized query and correct table name
    #             query = text("""
    #                 SELECT * FROM equipments_booking 
    #                 WHERE student_email = :email
    #             """)
    #             result = conn.execute(query, {'email': data['email_login']}).fetchall()
                
    #             if not result:
    #                 print("No bookings found for student")
    #                 return []
                    
    #             return result
                
    #     except Exception as e:
    #         print(f"Database error: {str(e)}")
    #         # Return empty list instead of crashing
    #         return []


    # def delete_booking_from_db(self ,data):
    #     print("This is important data and data = = = " , data)
    #     print(data[2])
    #     with self.engine.connect() as conn:                
    #             query3 = text(f"DELETE From equipments_booking where product_name = '{data[0]}' And product_type = '{data[1]}' And student_email = '{data[2]}';")
    #             conn.execute(query3)
    #             print("They all run goood")
    #     return True
