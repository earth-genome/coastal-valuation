import numpy as np


def discount(elev, slr, discount_rate=0.05):
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
