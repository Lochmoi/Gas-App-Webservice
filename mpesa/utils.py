from datetime import datetime


def get_timestamp():
    unformatted_time = datetime.now()
    formatted_time = unformatted_time.strftime("%Y%m%d%H%M%S")

    return formatted_time

def change_phone_no_format(phone_no_with_zero):
    with_zero_list = list(phone_no_with_zero)
    with_zero_list[0] = "254"
    result = "".join(with_zero_list)  # Change the list back to string, by using 'join' method of strings.
    print(f"Phone number that has been used is:{result}")
    return result