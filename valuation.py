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

    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('rate', type=float, required=False)
    parser.add_argument('address', required=True)
    parser.add_argument('city', required=True)
    parser.add_argument('state', required=True)
    parser.add_argument('zipcode', required=True)

    args = parser.parse_args()

    # Collect results

    house = housing.value(
        args['address'],
        args['city'],
        args['state'],
        args['zipcode']
    )

    depth = coastal.slr_depth(house['lat'], house['lon'])

    # If there is no rate passed to the query, assume we choose the default
    # from a joint probability distribution of SLR derived from scientific
    # surveys
    if args['rate'] is None:
        discount, years = climate.joint_prob_discount(depth)
    else:
        discount, years = climate.discount(depth, args['rate'])

    # Format and return results

    def _fmt(val):
        # lightweight, anonymous function to format housing prices as a string
        return '${:,.2f}'.format(val)

    house_attrs = {
        'lat': house['lat'],
        'lon': house['lon'],
        'valuation': _fmt(house['valuation'])
    }

    adj_value = _fmt(discount * house['valuation'])

    return json.dumps({
        'version': version,
        'result': {
            'adjusted_valuation': adj_value,
            'house': house_attrs
        }
    })


@app.route('/<version>/')
def coastal_docs(version):
    # Documentation
    with open('web/docs.json') as docs:
        data = json.load(docs)

    data['version'] = version

    return json.dumps(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
