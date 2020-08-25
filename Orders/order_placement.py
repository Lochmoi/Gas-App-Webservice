import datetime
import pytz
import json
from Orders import prices, random_order_no_generator
from CustomDatetime.convert_datetime_str import convert_str
from mpesa.lipa_na_mpesa import lipa_na_mpesa

def place_order(order_data, db, order_details_model):

    try:
        placed_time = convert_str(datetime.datetime.now().isoformat())
        order_number = random_order_no_generator.create_random_order_no("Gas", "Juja")

        order_servicing = "current" # Current or scheduled. Remove hardcoding later


        # Fetching the price for the particular order

        order_type = order_data['order_type']
        brand = order_data['brand']
        size = order_data['size']

        price = prices.fetch_price(order_type,brand,size)


        other_order_data ={
        "order_servicing": order_servicing,
        "placed_time": placed_time,
        "order_status": "pending",
        "partner_alerted": "False",
        "order_number": order_number,
        "delayed": "false",
        "amount": price
        }
        
        #Change "location" to json strings from dicts


        order_data["location"] = json.dumps(order_data["location"])


        #Store order persistently in db
        
        new_order = order_details_model(order_no= order_number, name=order_data['name'], phone_no=order_data['phone_no'], order_servicing= order_servicing,
                                        size=order_data['size'], brand=order_data['brand'], order_type=order_data['order_type'],
                                    location=order_data['location'], placed_time= placed_time, date_time=order_data['date_time'], complete="Pending", 
                                    amount= price)
        db.session.add(new_order)
        db.session.commit()

        message = "Order has been placed succesfully"

        # Trigger mpesa stkpush
        lipa_na_mpesa(order_data['phone_no'], price)

        response =  order_number, message, price

        return response

    except Exception as e:
        print(f'[x] Could not place order. Error: {e}')
        message = "An error occured while placing your order. Please try again"
        order_number = None
        price = None
        response = order_number, message, price

        return response

def get_price(order_data):
    print(order_data)
    print(type(order_data))
    order_type=order_data['order_type']
    brand=order_data['brand']
    size=order_data['size']

    price = prices.fetch_price(order_type,brand,size)
    message = "Price fetched"

    response = message, price

    return response