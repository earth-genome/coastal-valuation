import config
import requests
from bs4 import BeautifulSoup


def value(address, city, state, zipcode):
    """

    Query the Zillow API to get the estimate and geographical coordinates of
    the supplied address.

    """
    zillow_base = config.urls['zillow_search']
    zillow_payload = {
        'zws-id': config.keys['zillow'],
        'address': address,
        'citystatezip': '+'.join([city, state, zipcode]),
        'zestimate': 'true'
    }
    a = requests.get(zillow_base, params=zillow_payload)
    soup = BeautifulSoup(a.content, "html.parser")

    lon = float(soup.find('longitude').contents[0])
    lat = float(soup.find('latitude').contents[0])
    valuation = int(soup.find('zestimate').find('amount').contents[0])

    return {'lon': lon, 'lat': lat, 'valuation': valuation}
