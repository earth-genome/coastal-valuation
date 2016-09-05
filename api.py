import json
import webapp2
from main import geocode


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
        res = geocode(address, city, state, zipcode)
        self.response.write(json.dumps(res))


handlers = webapp2.WSGIApplication(
    [
        ('/', AddressHandler)
    ], debug=True
)
