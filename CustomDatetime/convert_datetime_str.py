def convert_str(date_time_string):
    try:
        full_string_split = date_time_string.split(".")[0]
        split_with_T = full_string_split.split("T")
        standard_string = f'{split_with_T[0]} {split_with_T[1]}'
        return standard_string
    except Exception as e:
        print(f"Could not convert times string to standard dt string. Error: {e}")
        return date_time_string