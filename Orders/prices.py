def fetch_price(order_type,brand,size):

    order_type_lowercase = order_type.lower()
    brand_lowercase = other_brand(brand).lower()
    size_lowercase = size.lower()

    order = f'{order_type_lowercase}_{brand_lowercase}_{size_lowercase}'

    prices = {
        "purchase_total_3kg": "2400",
        "purchase_total_6kg": "4000",
        "purchase_total_13kg": "7000",
        "purchase_kgas_3kg": "2500",
        "purchase_kgas_6kg": "4200",
        "purchase_kgas_13kg": "7000",
        "purchase_progas_3kg": "2000",
        "purchase_progas_6kg": "3500",
        "purchase_progas_13kg": "6000",
        "purchase_other_3kg": "3000",
        "purchase_other_6kg": "3900",
        "purchase_other_13kg": "6500",
        "refill_total_3kg": "400",
        "refill_total_6kg": "1000",
        "refill_total_13kg": "2000",
        "refill_kgas_3kg": "500",
        "refill_kgas_6kg": "1200",
        "refill_kgas_13kg": "2000",
        "refill_progas_3kg": "450",
        "refill_progas_6kg": "1000",
        "refill_progas_13kg": "2000",
        "refill_other_3kg": "400",
        "refill_other_6kg": "900",
        "refill_other_13kg": "1900",

    }

    price = prices.get(order)

    return price

#If the brand is not one of the well known brands, assign brand to "Other"

def other_brand(brand):
    
    if brand != "Total" and brand != "K-Gas" and brand != "Pro-Gas":
        brand = "Other"
    
    return brand

print(fetch_price("Refill","Hass","6kg"))