from math import sin, cos, atan2


# map the given angle to the equivalent angle in [ -pi, pi ]
def normalize_angle(theta):
    return atan2(sin(theta), cos(theta))


def frange(x, y, jump=1.0):
    r = []
    while x < y:
        r.append(x)
        x += jump

    return r
