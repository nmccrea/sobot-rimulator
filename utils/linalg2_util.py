from math import sqrt, sin, cos


# get the sum of two vectors
def add(a, b):
    return [a[0] + b[0], a[1] + b[1]]


# get the difference of two vectors ( a - b )
def sub(a, b):
    return [a[0] - b[0], a[1] - b[1]]


# multiply a vector a by a scalar s
def scale(a, s):
    return [s * a[0], s * a[1]]


# get the dot-product of two vectors
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


# get the cross-product of two vectors ( a x b )
def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


# get the magnitude of a vector
def mag(a):
    return sqrt(a[0] ** 2 + a[1] ** 2)


# get the unit vector of a vector
def unit(a):
    m = mag(a)
    return [a[0] / m, a[1] / m]


# get the right-hand normal of a vector
def rnormal(a):
    return [a[1], -a[0]]


# get the right-hand unit normal of a vector
def runormal(a):
    return unit([a[1], -a[0]])


# get the left-hand normal of a vector
def lnormal(a):
    return [-a[1], a[0]]


# get the left-hand unit normal of a vector
def lunormal(a):
    return unit([-a[1], a[0]])


# get the projection of vector a onto vector b
def proj(a, b):
    scale = float(dot(a, b)) / (b[0] ** 2 + b[1] ** 2)
    return [scale * b[0], scale * b[1]]


# get the length of the difference of two vectors a and b
def distance(a, b):
    return mag(sub(a, b))


# get the result of rotating a vector by theta radians
def rotate_vector(a, theta):
    sin_theta = sin(theta)
    cos_theta = cos(theta)

    a0 = a[0] * cos_theta - a[1] * sin_theta
    a1 = a[0] * sin_theta + a[1] * cos_theta

    return [a0, a1]


# get the result of rotating a set of vectors by theta radians
def rotate_vectors(vects, theta):
    sin_theta = sin(theta)
    cos_theta = cos(theta)

    rotvects = []
    for a in vects:
        a0 = a[0] * cos_theta - a[1] * sin_theta
        a1 = a[0] * sin_theta + a[1] * cos_theta
        rotvects.append([a0, a1])

    return rotvects


# get the result of rotating and translating a vector
def rotate_and_translate_vector(a, theta, tvect):
    return add(rotate_vector(a, theta), tvect)


# get the result of rotating and translating a set of vectors
def rotate_and_translate_vectors(vects, theta, tvect):
    rtvects = []
    for a in rotate_vectors(vects, theta):
        rtvects.append(add(a, tvect))

    return rtvects


# determine which side of a line a point lies on
def determine_side_of_line(lpoint1, lpoint2, tpoint):
    # returns  1 if the point is to the left of the line
    # returns -1 if the point is to the right of the line
    # returns  0 if the point is on the line
    # the directionality of the line is taken to be lpoint1 -> lpoint2
    tx = tpoint[0]
    ty = tpoint[1]
    l1x = lpoint1[0]
    l1y = lpoint1[1]
    l2x = lpoint2[0]
    l2y = lpoint2[1]

    d = (ty - l1y) * (l2x - l1x) - (tx - l1x) * (l2y - l1y)

    return d if d == 0 else int(d / abs(d))
