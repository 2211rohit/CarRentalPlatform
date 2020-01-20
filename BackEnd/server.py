#! /usr/bin/python3

from flask import Flask
from flask_cors import CORS
from flask import request, make_response, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
import json
import hashlib
import jwt
import os
import math
app = Flask(__name__, static_url_path="/static")
CORS(app)

app.config["MYSQL_USER"] = "rohit"
app.config["MYSQL_PASSWORD"] = "Goyal@123"
app.config["MYSQL_DB"] = "carRental"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


# 1. hash
def _md5_hash(string):
    hash = hashlib.md5()
    hash.update(string.encode("utf-8"))
    return hash.hexdigest()


# 2. salt
def _generate_salt():
    salt = os.urandom(16)
    return salt.hex()


# 3. Token Decode
def _token_decode(token_encoded):
    decode_data = jwt.decode(token_encoded, "secret", algorithms=["HS256"])
    return decode_data


# 4. global select def
def alldata(query):
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


# 5. global select def with some condition
def _conditional_data(query, value):
    cursor = mysql.connection.cursor()
    cursor.execute(query, value)
    results = cursor.fetchall()
    cursor.close()
    return results


# 6. global insert,update,delete def
def _insert_data(query, values):
    print(query)
    cursor = mysql.connection.cursor()
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()
    return {"message": True}


# API Calls
# 1. SIGNUP API
@app.route("/signup", methods=["POST"])
def create_user():
    name = request.json["name"]
    email = request.json["email"]
    number = request.json["number"]
    user_password = request.json["password"]
    user_license = request.json["license"]
    salt = "dummy_salt"
    password = _md5_hash(user_password)
    all_users = "select * from user"
    users = alldata(all_users)
    for i in users:
        if email == i["user_email"]:
            return {"message": "Email already registered"}
    else:
        add_query = """INSERT INTO user (user_name, user_email, user_number, user_password, user_salt, user_license) values (%s, %s, %s, %s, %s, %s)"""
        value_list = [name, email, number, password, salt, user_license]
        return _insert_data(add_query, value_list)

# 2. LOGIN API
@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]
    current_query = "Select * from user"
    users = alldata(current_query)
    for i in users:
        if email == i["user_email"]:
            salt = i["user_salt"]
            password = _md5_hash(password)
            if password == i["user_password"]:
                encode_data = jwt.encode(
                    {"user_id": i["user_id"]}, "secret", algorithm="HS256")
                get_query = "select * from user where user_id = %s"
                value = [i["user_id"]]
                return {"data": {"token": str(encode_data), "user": _conditional_data(get_query, value)}}
    else:
        return {"data": "Email Not Registered"}


# 3. GET ALL CARS
@app.route("/cars", methods=["POST"])
def cars():
    auth_header = request.headers.get("Authorization")
    token_encoded = auth_header.split(" ")[1]
    decode_data = _token_decode(token_encoded)
    user_id = request.json["user_id"]
    user_car_query = """select car_id, car_model, car_type, car_seats, car_color, car_booked from Cars"""
    cars = all_data(user_car_query)
    return {"data": cars}


# 4. GET ALL BOOKINGS OF A USER
@app.route("/bookings", methods=["POST"])
def user_bookings():
    auth_header = request.headers.get("Authorization")
    print(auth_header)
    # token_encoded = auth_header.split(" ")[1]
    # decode_data = _token_decode(token_encoded)
    user_id = request.json["user_id"]
    # if user_id == decode_data["user_id"]:
    user_bookings = """select * from Booking join Cars on Cars.car_id = Booking.car_id where user_id = %s"""
    value = [user_id]
    bookings = _conditional_data(user_bookings, value)
    return {"data": bookings}
    # else:
    #     return {"message": False}


# 5. BOOK A CAR
@app.route("/bookCar", methods=["POST"])
def add_booking():
    # auth_header = request.headers.get("Authorization")
    # token_encoded = auth_header.split(" ")[1]
    # decode_data = _token_decode(token_encoded)
    user_id = request.json["user_id"]
    date = request.json["date"]
    days = request.json["days"]
    # if user_id == decode_data["user_id"]:
    car_id = request.json["car_id"]
    add_booking = """INSERT INTO Booking(user_id, car_id, booking_date, booking_days) values (%s, %s, %s, %s)"""
    values = (user_id, car_id, date, days)
    car_booking = """UPDATE Cars SET car_booked = %s WHERE car_id = %s"""
    value = ("1", car_id)
    booked = _insert_data(add_booking, values)
    car_booked = _insert_data(car_booking, value)
    if booked["message"] == True and car_booked["message"] == True:
        return {"message": "Success"}
    else:
        return {"message": "Invalid User Request"}


# 6. GET USER DATA
@app.route("/userData", methods=["POST"])
def data_user():
    auth_header = request.headers.get("Authorization")
    token_encoded = auth_header.split(" ")[1]
    decode_data = _token_decode(token_encoded)
    user_id = request.json["user_id"]
    if user_id == decode_data["user_id"]:
        query = "select user_id, user_name, user_email, user_number from user"
        return {"data": alldata(query)}
    else:
        return {"message": "Invalid User Request"}

# 7. ADD A CAR
@app.route("/addCar", methods=["POST"])
def add_car():
    car_model = request.json["model"]
    car_type = request.json["type"]
    car_seats = request.json["seats"]
    car_color = request.json["color"]
    car_booked = "0"
    add_car = """INSERT INTO Cars(car_model, car_type, car_seats, car_color, car_booked) values (%s, %s, %s, %s, %s)"""
    values = (car_model, car_type, car_seats, car_color, car_booked)
    return _insert_data(add_car, values)


# 8. GET ALL NON BOOKED CARS
@app.route("/allcars", methods=["POST"])
def all_cars():
    user_car_query = """select car_id, car_model, car_type, car_seats, car_color, car_booked from Cars WHERE car_booked = %s"""
    values = ("0")
    cars = _conditional_data(user_car_query, values)
    return {"data": cars}

# 9. COMPLETE A BOOKING
@app.route("/delBook", methods=["DELETE"])
def del_booking():
    # auth_header = request.headers.get("Authorization")
    # token_encoded = auth_header.split(" ")[1]
    # decode_data = _token_decode(token_encoded)
    user_id = request.json["user_id"]
    car_id = request.json["car_id"]
    booking_id = request.json["booking_id"]
    # if user_id == decode_data["user_id"]:
    del_booking = """DELETE FROM Booking WHERE booking_id = %s"""
    values = (booking_id)
    car_booking = """UPDATE Cars SET car_booked = %s WHERE car_id = %s"""
    value = ("0", car_id)
    booked = _insert_data(del_booking, values)
    car_booked = _insert_data(car_booking, value)
    if (booked["message"] == True and car_booked["message"] == True):
        return {"message": "Success"}
    else:
        return {"message": "Invalid User Request"}
