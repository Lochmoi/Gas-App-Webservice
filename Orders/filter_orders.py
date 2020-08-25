# Module for filtering of orders
from sqlalchemy import desc


def filter(req_data, order_details_model):
    criteria = req_data['criteria']
    payload = req_data['payload']

    if criteria == "order_type":
        result = order_details_model.query.filter_by(order_type=payload).order_by(desc(order_details_model.id))
    elif criteria == "gate":
        result = order_details_model.query.filter_by(gate_region=payload).order_by(desc(order_details_model.id))
    elif criteria == "phone_no":
        result = order_details_model.query.filter_by(phone_no=payload).order_by(desc(order_details_model.id))
    elif criteria == "date":
        result = order_details_model.query.filter_by(placed_time=payload).order_by(desc(order_details_model.id))
    else:
        result = "Error fetching filtered orders"

    return result