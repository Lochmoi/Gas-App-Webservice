def get_orders(orders):
    
    orders_array = []

    for order in orders:
        order_data = {}
        order_data['order_no'] = order.order_no
        order_data['name'] = order.name
        order_data['phone_no'] = order.phone_no
        order_data['order_type'] = order.order_type
        order_data['brand'] = order.brand
        order_data['size'] = order.size
        order_data['location'] = order.location
        order_data['placed_time'] = order.placed_time
        order_data['date_time'] = order.date_time
        order_data['order_servicing'] = order.order_servicing
        order_data['complete'] = order.complete
        order_data['amount'] = order.amount
        orders_array.append(order_data)
    
    return orders_array
