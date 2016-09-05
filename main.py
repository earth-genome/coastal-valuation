import json
import urllib
from google.appengine.api import urlfetch


def geocode(address, city, state, zipcode):
    base = 'http://sampleserver1.arcgisonline.com/ArcGIS/rest/services/'
    d = 'Locators/ESRI_Geocode_USA/GeocodeServer/findAddressCandidates'

    payload = {
        'Address': address,
        'City': city,
        'State': state,
        'Zip': zipcode,
        'f': 'json'
    }

    url = base + d + '?' + urllib.urlencode(payload)
    data = json.loads(urlfetch.fetch(url=url).content)
    coords = data['candidates'][0]['location']
    lat = coords['y']
    lon = coords['x']

    return {
        'response': {
            'lat': lat,
            'lon': lon
        }
    }
