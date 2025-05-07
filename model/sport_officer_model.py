import json
from flask import flash
from flask import make_response, render_template
from sqlalchemy import create_engine, text
import os
from datetime import datetime
import datetime

class sport_officer_model():
    engine = None

    def __init__(self):
        try:
            self.engine = create_engine("mysql+pymysql://root@127.0.0.1:3306/Paf_Iast_EMS")

            print("connection built successfully")
        except:
            print("not working")


                

    def add_new_equipments_to_db(self, data: dict, image_path: str) -> bool:
        try:
            with self.engine.begin() as conn:  # Auto-commit/rollback transaction
                # Check existing equipment
                check_query = text("""
                    SELECT * FROM equipments 
                    WHERE product_name = :name 
                    AND type_of_product = :type
                """)
                result = conn.execute(check_query, {
                    'name': data['product_name'],
                    'type': data['type_of_product']
                }).fetchone()

                if result:
                    # Update existing equipment
                    update_query = text("""
                        UPDATE equipments SET
                            quantity_of_product = quantity_of_product + :qty,
                            avaiable_product = avaiable_product + :qty,
                            descipation = :desc,
                            image_of_product = :img
                        WHERE product_name = :name
                        AND type_of_product = :type
                    """)
                    conn.execute(update_query, {
                        'qty': data['quantity_of_product'],
                        'desc': data['descipation'],
                        'img': image_path,
                        'name': data['product_name'],
                        'type': data['type_of_product']
                    })
                    print("Existing equipment updated")
                else:
                    # Insert new equipment
                    insert_query = text("""
                        INSERT INTO equipments 
                        (product_name, quantity_of_product, avaiable_product,
                        type_of_product, descipation, image_of_product)
                        VALUES (:name, :qty, :avail, :type, :desc, :img)
                    """)
                    conn.execute(insert_query, {
                        'name': data['product_name'],
                        'qty': data['quantity_of_product'],
                        'avail': data['quantity_of_product'],  # Initial available = total
                        'type': data['type_of_product'],
                        'desc': data['descipation'],
                        'img': image_path
                    })
                    print("New equipment added")

                return True

        except Exception as e:
            print(f"Database error: {str(e)}")
            return False
        



    def take_booking_data_form_db(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * From equipments_booking;")
            cheek = conn.execute(query1).fetchall()
            return cheek
        


    def take_booking_approval_data_form_db(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * From equipments_booking_approved;")
            cheek = conn.execute(query1).fetchall()
            return cheek
        
        
        
    def send_approved_booking_data_to_db(self, data):
        print("Processing approval for:", data)
        try:
            with self.engine.begin() as conn:  # Transaction starts
                # 1. Update equipment availability
                update_equipment = text("""
                    UPDATE equipments 
                    SET avaiable_product = avaiable_product - :quantity 
                    WHERE product_name = :name 
                    AND type_of_product = :type
                """)
                conn.execute(update_equipment, {
                    'quantity': data[4],
                    'name': data[0],
                    'type': data[1]
                })

                # 2. Insert into approved bookings (with correct table name)
                insert_approved = text("""
                    INSERT INTO equipments_booking_approved 
                    (product_name, product_type, student_email,
                    booking_time, number_of_products, image_path)
                    VALUES (:name, :type, :email, :time, :qty, :img)
                """)
                conn.execute(insert_approved, {
                    'name': data[0],
                    'type': data[1],
                    'email': data[2],
                    'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'qty': data[4],
                    'img': data[5]
                })


                # 3. Remove from pending bookings
                delete_pending = text("""
                    DELETE FROM equipments_booking 
                    WHERE product_name = :name 
                    AND product_type = :type 
                    AND student_email = :email
                """)
                conn.execute(delete_pending, {
                    'name': data[0],
                    'type': data[1],
                    'email': data[2]
                })

                print("Approval processed successfully")
                return True

        except Exception as e:
            print(f"Approval failed: {str(e)}")
            return False
        
    # def cancle_booking_data_from_db(self , data):
        print("This isj oifaj o data = = - = = " , data)
        print("This isj oifaj o data = = - = = " , data[0])
        with self.engine.connect() as conn:
            query1 = text(f"Update  equipments  SET  avaiable_product = (avaiable_product + {data[4]})  WHERE product_name = '{data[0]}' AND type_of_product = '{data[1]}';")
            conn.execute(query1)
            
            query2 = text(f"DELETE FROM equipments_booking_approved WHERE product_name = '{data[0]}' AND product_type = '{data[1]}' AND student_email = '{data[2]}' AND number_of_products = {data[4]} ;")
            conn.execute(query2)
            return True
        

    def cancle_booking_data_from_db(self, data):
        print("Cancelling booking:", data)
        try:
            with self.engine.begin() as conn:
                # 1) restore availability
                conn.execute(
                    text("""
                        UPDATE equipments
                        SET avaiable_product = avaiable_product + :qty
                        WHERE product_name = :name
                        AND type_of_product = :type
                    """),
                    {
                        "qty": data[4],
                        "name": data[0],
                        "type": data[1]
                    }
                )

                # 2) delete the approved booking
                conn.execute(
                    text("""
                        DELETE FROM equipments_booking_approved
                        WHERE product_name = :name
                        AND product_type = :type
                        AND student_email = :email
                        AND number_of_products = :qty
                    """),
                    {
                        "name": data[0],
                        "type": data[1],
                        "email": data[2],
                        "qty": data[4]
                    }
                )

            print("Cancellation committed")
            return True

        except Exception as e:
            print("Error cancelling booking:", e)
            return False



    def stored_image_in_file_and_send_path_in_db(self , file , folder_name):
        if file is not None:
            # new_filename = str(datetime.now().timestamp()).replace(".", "")  # Generating unique name for the file
            new_filename = str(datetime.datetime.now().timestamp()).replace(".", "")
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