import mysql.connector
import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
import mysql.connector
from datetime import datetime



class sport_officer_model():
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


                
    def add_new_equipments_to_db(self , data , image_path):
        print("The data os s = = = =", data)
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * From equipments where product_name = '{data['product_name']}' AND type_of_product = '{data['type_of_product']}';")
            cheek = conn.execute(query1).fetchall()
            if cheek:
                query2 = text(f"Update  equipments  SET product_name = '{data['product_name']}', quantity_of_product =  ({data['quantity_of_product']} + quantity_of_product), avaiable_product = ({data['quantity_of_product']} + avaiable_product), type_of_product =  '{data['type_of_product']}', descipation = '{data['descipation']}'  ,image_of_product = '{image_path}' WHERE product_name = '{data['product_name']}' AND type_of_product = '{data['type_of_product']}';")
                conn.execute(query2)


                print("Its diffiect aisgj ")
            else:
                query2 = text(f"INSERT INTO equipments VALUES ('{data['product_name']}', {data['quantity_of_product']} , {data['quantity_of_product']}, '{data['type_of_product']}', '{data['descipation']}', '{image_path}');")
                conn.execute(query2)
                print("its eassu")
            print("it also works")
            return True
        
        
    def take_booking_data_form_db(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * From equipmetns_booking;")
            cheek = conn.execute(query1).fetchall()
            return cheek
        
    def cancle_booking_data_from_db(self , data):
        print("This isj oifaj o data = = - = = " , data)
        print("This isj oifaj o data = = - = = " , data[0])
        with self.engine.connect() as conn:
            query1 = text(f"Update  equipments  SET  avaiable_product = (avaiable_product + {data[4]})  WHERE product_name = '{data[0]}' AND type_of_product = '{data[1]}';")
            conn.execute(query1)
            
            query2 = text(f"DELETE FROM equipmetns_booking WHERE product_name = '{data[0]}' AND product_type = '{data[1]}' AND student_email = '{data[2]}' AND number_of_products = {data[4]} ;")
            conn.execute(query2)
            return True
        





    def stored_image_in_file_and_send_path_in_db(self , file , folder_name):
        if file is not None:
            new_filename = str(datetime.now().timestamp()).replace(".", "")  # Generating unique name for the file
            # Spliting ORIGINAL filename to seperate extenstion
            split_filename = file.filename.split(".")
            # Canlculating last index of the list got by splitting the filname
            ext_pos = len(split_filename)-1
            # Using last index to get the file extension
            ext = split_filename[ext_pos]
            img_db_path = str(f"{folder_name}/{new_filename}.{ext}")
            print("The type of path  = ", type(img_db_path))
            file.save(f"static/{folder_name}/{new_filename}.{ext}")
            print("File uploaded successfully")
            return img_db_path
     
     
    def take_store_data_from_db(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * From equipments ORDER BY type_of_product ASC;")
            cheek = conn.execute(query1).fetchall()
            return cheek