from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
from sqlalchemy import *
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from Orders import order_placement, get_orders
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
    order_no = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))
    phone_no = db.Column(db.String(11))
    order_servicing = db.Column(db.String(10))
    placed_time = db.Column(db.String(30))
    date_time = db.Column(db.String(30))
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

                # return redirect(url_for('orders'))  # orders()
                response = jsonify(message="Successfully logged in")
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

        return render_template('signup.html')


@app.route('/complete_order_in_admin/<theid>', methods=['PUT', 'GET', 'POST'])
def complete_order_in_admin(theid):
    idd = theid

    Orderdetails.query.filter_by(id=idd).update(
        {Orderdetails.complete: "Completed"})
    db.session.commit()

    return redirect(url_for('admin'))


@app.route('/complete_order_in_latest/<theid>', methods=['PUT', 'GET', 'POST'])
def complete_order_in_latest(theid):
    idd = theid
    Orderdetails.query.filter_by(id=idd).update(
        {Orderdetails.complete: "Completed"})
    db.session.commit()

    return redirect(url_for('latest_orders'))


@app.route('/complete_order_in_pending/<theid>', methods=['PUT', 'GET', 'POST'])
def complete_order_in_pending(theid):
    idd = theid

    Orderdetails.query.filter_by(id=idd).update(
        {Orderdetails.complete: "Completed"})
    db.session.commit()
    return redirect(url_for('pending_orders'))


@app.route('/confirm_order')
@login_required
def confirm():
    return render_template('order_confirmation.html', name=current_user.name)


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
        orders = Orderdetails.query.all()

        orders_array = get_orders.get_orders(orders)
        return jsonify({'orders' : orders_array})

@app.route('/api/get_price', methods=['POST'])
def get_price():
    order_data = request.get_json()
    response = order_placement.get_price(order_data)
    
    return jsonify(message=response[0],  
                       price = response[1])


if __name__ == "__main__":
    app.run()
