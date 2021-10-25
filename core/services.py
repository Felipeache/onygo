from requests import post


def validate_address(event_address, city):
    if len(event_address) == 0 or len(city) == 0:
        return False
    else:
        event_address = event_address.replace(" ", "+").strip()
        city = city.replace(" ", "+").strip()
        geo_api = f"https://nominatim.openstreetmap.org/search?q={event_address}+{city}&format=json&polygon=1&addressdetails=1"
        api_response = post(geo_api).json()
        return True if len(api_response) > 0 else False


def get_lat_lon(event_address, city):
    event_address = event_address.replace(" ", "+").strip()
    city = city.replace(" ", "+").strip()
    geo_api = f"https://nominatim.openstreetmap.org/search?q={event_address}+{city}&format=json&polygon=1&addressdetails=1"
    api_response = post(geo_api).json()
    event_address, city = "", ""
    return f"{api_response[0]['lat']} {api_response[0]['lon']}"


def get_postal_code(event_address, city):
    event_address = event_address.replace(" ", "+").strip()
    city = city.replace(" ", "+").strip()
    geo_api = f"https://nominatim.openstreetmap.org/search?q={event_address}+{city}&format=json&polygon=1&addressdetails=1"
    api_response = post(geo_api).json()
    event_address, city = "", ""
    return f"{api_response[0]['address']['postcode']}"


def decode_lat_lon(lat_lon):
    lat, lon = lat_lon.split(" ")[0], lat_lon.split(" ")[1]
    decode_api = (
        f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    )
    api_response = post(decode_api).json()
    lat_lon = "", ""
    return api_response["address"]
