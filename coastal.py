import json
import urllib
from google.appengine.api import urlfetch


def slr_depth(lat, lon):
    """

    Returns the water depth (in feet) at high tide and at the supplied
    coordinates if sea level were to rise 6 ft for the supplied coordinate.

    Technical description:
        Potential inundation of 6 ft above current Mean Higher High Water
        (MHHW) as a result of sea level rise (in feet).  Levels represent
        inundation at high tide.

    Example:
        >>> slr_depth(32.862305, -79.919835)
        0.385538

    Reference:
        https://coast.noaa.gov/slr

    """
    base_server = 'http://earthgenomevm.cloudapp.net:6080/'
    img_server = 'arcgis/rest/services/SLR_Depth_6ft/ImageServer/identify'
    url_base = base_server + img_server

    # filter out unnecessary images with the `mosaicRule` field-value pair
    # (i.e., there are many unneccesary images on Arc Image Servers that start
    # with 'Ov', presumably meta files)
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
