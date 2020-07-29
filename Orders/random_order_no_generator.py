import uuid

def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.

def create_random_order_no(business, location):
    business_code_names = {
        "Gas": "G"
    }
    #Four letter code words to appear in order number
    location_code_names= {
        "Juja": "JUJA",
        "MKU": "MKUU",
        "Daystar": "DYTR",
        "KU": "KUNI"
    }
    
    biz = business_code_names.get(business)
    loc = location_code_names.get(location)
    random_string = my_random_string(10)

    order_number = f'{biz}{loc}-{random_string}'

    return order_number