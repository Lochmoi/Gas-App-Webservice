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
        order_data['gate_region'] = order.gate_region
        order_data['apartment'] = order.apartment
        order_data['date_placed'] = order.date_placed
        order_data['time_placed'] = (order.time_placed).split(".")[0]
        order_data['complete'] = order.complete
        orders_array.append(order_data)
    
    return orders_array
