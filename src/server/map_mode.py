import math
from motor.engine_test import backward, forward, turn_left, turn_right, stop

def calculate_distance(coord1, coord2):
    # Calculate the distance between two points using the Haversine formula
    R = 6371000  # Radius of the Earth in Metters
    lat1, lon1 = math.radians(coord1["latitude"]), math.radians(coord1["longitude"])
    lat2, lon2 = math.radians(coord2["latitude"]), math.radians(coord2["longitude"])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def calculate_bearing(coord1, coord2):
    # Calculate the bearing between two points
    lat1, lon1 = math.radians(coord1["latitude"]), math.radians(coord1["longitude"])
    lat2, lon2 = math.radians(coord2["latitude"]), math.radians(coord2["longitude"])
    dlon = lon2 - lon1

    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    bearing = math.degrees(math.atan2(x, y))
    bearing = (bearing + 360) % 360
    return bearing

