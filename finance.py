import numpy as np
from decimal import *


def discount(T, rate=0.05):
    run = np.repeat(1, 1000)
    buf = np.repeat(0, T)
    lost = np.append(buf, np.repeat(1, 1000 - T))
    return 1 - (np.npv(rate, lost) / np.npv(rate, run))


def moneyfmt(value):
    """

    Accepts an integer or float value representing a home price, and returns a
    human-readable string, with dollar sign.  Not generally extensible.  Meant
    to format positive valuations of houses.

    Example:

        >>> moneyfmt(123456.78)
        '$123,456.78'

    """

    if type(value) != 'str':
        value = str(value)

    q = Decimal(10) ** -2
    sign, digits, exp = Decimal(value).quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, next = result.append, digits.pop
    if sign:
        build('')
    for i in range(2):
        build(next() if digits else '0')

    build('.')

    if not digits:
        build('0')

    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(',')
    build('$')
    build('-' if sign else '')
    return ''.join(reversed(result))
