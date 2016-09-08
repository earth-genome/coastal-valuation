import json
import urllib
import sys
sys.path.insert(0, 'libs')

from bs4 import BeautifulSoup
from google.appengine.api import urlfetch


def geocode(address, city, state, zipcode):
    """

    400 Balboa Blvd,
    Half Moon Bay, CA 94019

    """
    # Check zestimate, Earth Genome Developer API key
    zillow_base = 'http://www.zillow.com/webservice/GetSearchResults.htm'
    zillow_payload = {
        'zws-id': 'X1-ZWz19l1vnzxtzf_ac8os',
        'address': address.replace(" ", "+"),
        'citystatezip': '+'.join([city, state, zipcode]),
        'zestimate': 'true'
    }

    zillow_url = zillow_base + '?' + urllib.urlencode(zillow_payload)
    zillow_data = urlfetch.fetch(url=zillow_url).content
    soup = BeautifulSoup(zillow_data)

    lon = float(soup.find('longitude').contents[0])
    lat = float(soup.find('latitude').contents[0])

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
            'reference': lon
        }
    }

