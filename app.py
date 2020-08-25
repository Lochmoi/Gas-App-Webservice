from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
from sqlalchemy import *
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from Orders import order_placement, get_orders, filter_orders
import json


app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:512104013N@localhost/micahdb'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wfqtyftybqcbno:5c9e8c395e6497c55462194b5c37e097213125ec8992374c8106c7fae94c4005@ec2-52-44-166-58.compute-1.amazonaws.com:5432/d57mm50mhhl8ko'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['SECRET_KEY'] = '512104013N'
CORS(app)

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define models


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    phone_no = db.Column(db.String(11))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(80))


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    phone_no = db.Column(db.String(11))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(80))


class Orderdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(20))
    name = db.Column(db.String(50))
    phone_no = db.Column(db.String(11))
    order_servicing = db.Column(db.String(10))
    placed_time = db.Column(db.String(30))
    date_time = db.Column(db.String(30))
    size = db.Column(db.String(10))
    brand = db.Column(db.String(20))
    order_type = db.Column(db.String(20))
    complete = db.Column(db.String(10))
    location = db.Column(db.JSON, default={})
    amount = db.Column(db.Integer)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_data = request.get_json()

        user = User.query.filter_by(phone_no=user_data['phone_no']).first()

        if user:
            if user_data['password'] == user.password:
                login_user(user)
                user_name = user.name
                # get user phone number from login details

                # return redirect(url_for('orders'))  # orders()
                response = jsonify(message="Successfully logged in", name=user_name)
                return response
        response = jsonify(message="Invalid username/password combination")
        return response

    # Check out this part for get requests to the login route
    return render_template('login.html')


@app.route('/admin_login', methods=['POST', 'GET'])
def login_admin():
    if request.method == 'POST':

        admin_data = request.get_json()

        admin = Admin.query.filter_by(
            phone_no=admin_data['phone_no']).first()

        if admin:
            if admin_data['password'] == admin.password:

                response = jsonify(message = "Success")

                return response
        
        response = jsonify(message = "Invalid username/password combination")
        return response
    return render_template('admin_login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':

        new_user_data = request.get_json()

        name = new_user_data['name']
        email = new_user_data['email']
        phone_no = new_user_data['phone_no']
        password = new_user_data['password']

        new_user = User(name=name, phone_no=phone_no,
                        email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        response = jsonify(message = "User created")

        return response

    else:

        return jsonify(message= "Error found")



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#Endpoints for the api

@app.route('/api/orders', methods=['POST', 'GET'])
def api_orders():
    if request.method == 'POST':

        order_data = request.get_json()
    
        response = order_placement.place_order(order_data, db, Orderdetails)

        return jsonify(order_no = response[0], message=response[1], price = response[2])

    elif request.method == 'GET':
        orders = Orderdetails.query.order_by(desc(Orderdetails.id))

        orders_array = get_orders.get_orders(orders)
        return jsonify({'orders' : orders_array})

#For lastest

@app.route('/api/latest_orders')
def latest_orders():
    latest_orders = Orderdetails.query.order_by(desc(Orderdetails.id)).limit(5)
    orders_array = get_orders.get_orders(latest_orders)
    return jsonify({'orders' : orders_array})

@app.route('/api/pending_orders')
def pending_orders():
    pending_orders = Orderdetails.query.filter_by(
        complete='Pending').order_by(desc(Orderdetails.id))
    orders_array = get_orders.get_orders(pending_orders)
    return jsonify({'orders' : orders_array})

@app.route('/complete_order/<order_no>', methods=['PUT', 'GET', 'POST'])
def complete_order(order_no):

    Orderdetails.query.filter_by(order_no=order_no).update(
        {Orderdetails.complete: "Completed"})
    db.session.commit()

    return jsonify(message="Succesfully completed")


@app.route('/api/get_price', methods=['POST'])
def get_price():
    order_data = request.get_json()
    response = order_placement.get_price(order_data)
    
    return jsonify(message=response[0],  
                       price = response[1])

@app.route('/api/filter', methods=['POST'])
def filter():
    req_data = request.get_json()
    orders = filter_orders.filter(req_data, Orderdetails)
    orders_array = get_orders.get_orders(orders)
    return jsonify({'orders': orders_array})

if __name__ == "__main__":
    app.run()
