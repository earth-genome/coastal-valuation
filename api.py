import json
import webapp2
from main import discount_value, discount_rate


class AddressHandler(webapp2.RequestHandler):
    def get(self):

        # headers
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'

        # parameters
        address = self.request.get('address')
        city = self.request.get('city')
        state = self.request.get('state')
        zipcode = self.request.get('zip')

        # response
        res = discount_value(address, city, state, zipcode)
        self.response.write(json.dumps(res))


class DocsHandler(webapp2.RequestHandler):
    def get(self):

        # headers
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'

        # response
        res = {
            'service owner': 'Earth Genome',
            'objective': 'Provide the risk-adjusted value of coastal housing when incorporating projected sea level rise as a result of climate change',
            'sources': {
                'sea level rise': {
                    'author': 'NOAA',
                    'reference': 'https://coast.noaa.gov/data/digitalcoast/pdf/slr-faq.pdf'
                },
                'housing value': {
                    'author': 'Zillow',
                    'reference': 'http://www.zillow.com/zestimate'
                },
                'climate projections': {
                    'author': 'IPCC',
                    'reference': 'http://www.ipcc.ch/pdf/assessment-report/ar4/wg1/ar4-wg1-spm.pdf'
                }
            }
        }
        self.response.write(json.dumps(res))


handlers = webapp2.WSGIApplication(
    [
        ('/address', AddressHandler),
        ('/', DocsHandler)
    ], debug=True
)
