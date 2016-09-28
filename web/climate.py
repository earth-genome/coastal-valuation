import numpy as np


def slr_joint_prob_data(annualized=True):
    """

    SLR probability distribution (derived from the survey data) conditional on
    warming estimates, each of which has its own probability from the MIT/CAT
    numbers.  The raw data indicate the probability associated with aggregate
    sea level rise in centimeters (cm) by 2100, stored as a list of tuples of
    the form [SLR, probability].

    """
    raw = [
        [30, 0.00060],
        [40, 0.01014],
        [50, 0.04989],
        [60, 0.11846],
        [70, 0.17613],
        [80, 0.19034],
        [90, 0.16398],
        [100, 0.11964],
        [110, 0.07706],
        [120, 0.04513],
        [130, 0.02455],
        [140, 0.01261],
        [150, 0.00619],
        [160, 0.00293],
        [170, 0.00135],
        [180, 0.00061],
        [190, 0.00027],
        [200, 0.00012]
    ]

    # Years between projected date and the year of assessment.
    years = float(2100 - 2016)
    if annualized is True:
        return [[(x / years), y] for x, y in raw]
    else:
        return raw


def discount(elev, slr, discount_rate=0.025):
    """

    Accepts an elevation in feet and returns the discount factor associated
    with sea level rise (measured in centimeters per year)

    """
    # feet to centimeters with cm/year rise estimate. TODO: This is a rough,
    # terrible estimate and should be replaced to reflect actual science.
    T = ((6 - elev) / 0.0328084) / slr
    run = np.repeat(1, 1000)
    buf = np.repeat(0, T)
    lost = np.append(buf, np.repeat(1, 1000 - T))
    return 1 - (np.npv(discount_rate, lost) / np.npv(discount_rate, run)), T


def joint_prob_discount(elev, discount_rate=0.025):
    """

    Calculate the discount rate at a given elevation and discout rate, using
    the joint probability distribution of SLR derived from scientific survey.

    """

    discount_res = []
    time_res = []
    for [slr, prob] in slr_joint_prob_data():
        d, T = discount(elev, slr, discount_rate=discount_rate)
        discount_res.append(prob * d)
        time_res.append(prob * T)

    return sum(discount_res), sum(time_res)
