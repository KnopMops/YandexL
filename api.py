import random

import requests as req

API_KEY = ""

GEOCODE_URL = "https://geocode-maps.yandex.ru/1.x"
STATIC_URL = "https://static-maps.yandex.ru/1.x"

ZOOM_MIN = 13
ZOOM_MAX = 15
OFFSET_RANGE = 0.015
IMG_SIZE = "800, 600"


def geocode(address):
    params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json",
    }
    r = req.get(GEOCODE_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    members = data["response"]["GeoObjectCollection"]["featureMember"]
    if not members:
        return None, None

    obj = members[0]["GeoObject"]
    pos = obj["Point"]["pos"]
    lon, lat = map(float, pos.split())

    return (lon, lat), obj["name"]


def fetch_city_map(city_name):
    coords, resolved = geocode(city_name)

    if coords is None:
        raise ValueError()

    lon, lat = coords
    zoom = random.randint(ZOOM_MIN, ZOOM_MAX)
    lat += random.uniform(-OFFSET_RANGE, OFFSET_RANGE)
    lon += random.uniform(-OFFSET_RANGE, OFFSET_RANGE)

    params = {
        "apikey": API_KEY,
        "ll": f"{lon},{lat}",
        "z": zoom,
        "size": IMG_SIZE,
        "l": "map",
    }

    r = req.get(STATIC_URL, params=params, timeout=10)
    r.raise_for_status()

    return r.content, resolved
