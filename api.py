import json
import webapp2
from main import discount_value


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
        slr_rate = float(self.request.get('slr', 3.2))

        # response
        res = discount_value(address, city, state, zipcode, slr=slr_rate)
        self.response.write(json.dumps(res))


class DocsHandler(webapp2.RequestHandler):
    def get(self):

        # headers
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'

        # load json file
        with open('docs.json') as docs:
            data = json.load(docs)

        # response
        self.response.write(json.dumps(data))


handlers = webapp2.WSGIApplication(
    [
        ('/address', AddressHandler),
        ('/', DocsHandler)
    ], debug=True
)
