import json
from coastal_valuation import climate
from coastal_valuation import coastal
from coastal_valuation import housing

def valueAddress(address, city, state, zipcode):
    """

    Accepts an address of a U.S. property and returns the risk adjusted value,
    accounting for sea level rise.  

    Example:

    valueAddress("275 Beresford Creek Street", "Daniel Island", "SC","29492")
    
    {
        'adjusted_valuation': '$772,366.26', 
        'house': {
            'lat': 32.862305, 
            'valuation': '$788,037.00', 
            'lon': -79.919835
        }
    }

    """

    house = housing.value(address, city, state, zipcode)
    depth = coastal.slr_depth(house['lat'], house['lon'])

    # If there is no rate passed to the query, assume we choose the default
    # from a joint probability distribution of SLR derived from scientific
    # surveys

    discount, years = climate.joint_prob_discount(depth)

    def _fmt(val):
        # lightweight, anonymous function to format housing prices as a string
        return '${:,.2f}'.format(val)

    house_attrs = {
        'lat': house['lat'],
        'lon': house['lon'],
        'valuation': _fmt(house['valuation'])
    }

    adj_value = _fmt(discount * house['valuation'])

    return {
        'adjusted_valuation': adj_value,
        'house': house_attrs
    }