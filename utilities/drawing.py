from math import sqrt

def hex_to_rgb(hex):
    # https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    h = hex.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2 ,4))


def interpolate(colour_from, colour_to, t):
    r1, g1, b1 = colour_from
    r2, g2, b2 = colour_to

    r3 = r1 + (r2 - r1) * t
    g3 = g1 + (g2 - g1) * t
    b3 = b1 + (b2 - b1) * t

    return (r3, g3, b3)
