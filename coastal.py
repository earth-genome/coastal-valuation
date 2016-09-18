import json
import urllib
from google.appengine.api import urlfetch


def slr_depth(lat, lon):
    """

    Accepts a latitude and longitude, and returns the potential inundation of
    6 ft above current Mean Higher High Water (MHHW) as a result of sea level
    rise (in feet).  Levels represent inundation at high tide.

    Example:
        >>> slr_depth(32.862305, -79.919835)
        0.385538

    Reference:
        https://coast.noaa.gov/slr

    """
    base_server = 'http://earthgenomevm.cloudapp.net:6080/'
    img_server = 'arcgis/rest/services/SLR_Depth_6ft/ImageServer/identify'
    url_base = base_server + img_server

    # filter out unnecessary images
    payload = {
        'geometry': '{x:%s,y:%s}' % (lon, lat),
        'geometryType': 'esriGeometryPoint',
        'returnGeometry': 'false',
        'returnCatalogItems': 'false',
        'f': 'pjson',
        'mosaicRule': '{"where":"Name NOT LIKE \'Ov\%\'"}'
    }

    url = url_base + '?' + urllib.urlencode(payload)
    data = json.loads(urlfetch.fetch(url=url).content)

    if data['value'] == 'NoData':
        res = None
    else:
        res = float(data['value'])

    return res
