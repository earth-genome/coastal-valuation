import sys
import urllib
import finance
import coastal
import config
import climate
import numpy as np
from google.appengine.api import urlfetch

# Load local libraries
sys.path.insert(0, 'libs')
from bs4 import BeautifulSoup


def discount_value(address, city, state, zipcode, slr):
    """

    Discount the value based on going under water, given sea level rise rate.

    """
    # Check zestimate, Earth Genome Developer API key
    zillow_base = config.urls['zillow_search']
    zillow_payload = {
        'zws-id': config.keys['zillow'],
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

    # Spatial query to extract flood depth
    depth = coastal.slr_depth(lat, lon)
    discount_scalar, T = climate.discount(depth, slr)

    return {
        'response': {
            'coords': {
                'lat': lat,
                'lon': lon
            },
            'innundation': depth,
            'T': np.round(T, 2),
            'value': finance.moneyfmt(discount_scalar * valuation)
        },
        'meta': {
            'reference': finance.moneyfmt(valuation)
        }
    }
