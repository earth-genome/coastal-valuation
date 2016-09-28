import json
import climate
import coastal
import housing
import locale
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

    depth = coastal.slr_depth(32.862305, -79.919835)
    discount, years = climate.discount(depth, args['rate'])

    return json.dumps(
        {
            'version': version,
            'result': {
                'years': years,
                'adjusted_valuation': discount * house['valuation'],
                'house': house
            }
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
