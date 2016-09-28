import json
import climate
import coastal
import housing
from flask import Flask
from flask_restful import reqparse

app = Flask(__name__)


@app.route('/<version>/address')
def coastal_valuation(version):

    # Extract parameters
    parser = reqparse.RequestParser()

    parser.add_argument('rate', type=float, help='Rate must be a float.')
    parser.add_argument('address')
    parser.add_argument('city')
    parser.add_argument('state')
    parser.add_argument('zipcode')

    args = parser.parse_args()

    # Collect results
    house = housing.value(
        args['address'],
        args['city'],
        args['state'],
        args['zipcode']
    )

    depth = coastal.slr_depth(house['lat'], house['lon'])
    discount, years = climate.discount(depth, args['rate'])

    def _fmt(val):
        return '${:,.2f}'.format(val)

    return json.dumps(
        {
            'version': version,
            'result': {
                'years': years,
                'adjusted_valuation': _fmt(discount * house['valuation']),
                'house': {
                    'lat': house['lat'],
                    'lon': house['lon'],
                    'valuation': _fmt(house['valuation'])
                }
            }
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
