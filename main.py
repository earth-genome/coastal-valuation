import sys
import json
import urllib
import finance
from google.appengine.api import urlfetch

# Load local libraries
sys.path.insert(0, 'libs')
from bs4 import BeautifulSoup


def discount_value(address, city, state, zipcode):
    """
    Discount the value based on going under water
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
    soup = BeautifulSoup(zillow_data, "html.parser")

    lon = float(soup.find('longitude').contents[0])
    lat = float(soup.find('latitude').contents[0])
    valuation = int(soup.find('zestimate').find('amount').contents[0])

    # Spatial query to extract flood zones
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
    T = 35

    # check if list is empty
    if not flood_data['rows']:
        res = False
        flood_valuation = valuation
    else:
        res = True
        flood_valuation = valuation * finance.discount(T)

    return {
        'response': {
            'coords': {
                'lat': lat,
                'lon': lon
            },
            'flood': res,
            'value': finance.moneyfmt(str(flood_valuation), curr='$')
        },
        'meta': {
            'reference': finance.moneyfmt(str(valuation), curr='$')
        }
    }
