from geopy.geocoders import Nominatim

def geocode_address(address: str):
    geolocator = Nominatim(user_agent="WatchApp")
    location = geolocator.geocode(address, timeout=5)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None
