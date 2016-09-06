import json
import urllib
from google.appengine.api import urlfetch


def geocode(address, city, state, zipcode):
    """

    400 Balboa Blvd,
    Half Moon Bay, CA 94019

    """

    # Geocode address
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

    # Spatial query
    carto_base = 'https://danhammergenome.cartodb.com/api/v2/sql'

    sql = [
        'SELECT county ',
        'FROM ca_coast_yr2000_flood ',
        'WHERE ST_Intersects(',
            'the_geom::geography,',
            'CDB_LatLng(%s, %s)::geography' % (lat, lon),
        ')'
    ]
    sql_payload = {'q': ''.join(sql)}

    carto_url = carto_base + '?' + urllib.urlencode(sql_payload)
    flood_data = json.loads(urlfetch.fetch(url=carto_url).content)

    # check if list is empty
    if not flood_data['rows']:
        res = False
    else:
        res = True

    return {
        'response': {
            'coords': {
                'lat': lat,
                'lon': lon
            },
            'flood': res
        },
        'meta': {
            'reference': 'test'
        }
    }

