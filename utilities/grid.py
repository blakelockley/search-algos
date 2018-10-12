import numpy as np
import matplotlib.pyplot as plt
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


def progress(start, end, pos):
    total = sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
    length = sqrt((start[0] - pos[0]) ** 2 + (start[1] - pos[1]) ** 2)

    value = length / total

    return max(min(value, 1), 0)


def show_grid(data, path=[], side=20):
    _, ax = plt.subplots(figsize=(20, 10))

    ax.imshow(data)
    
    # Major ticks
    ax.set_xticks(np.arange(side))
    ax.set_yticks(np.arange(side))

    # Labels for major ticks
    ax.set_xticklabels(np.arange(side))
    ax.set_yticklabels(np.arange(side))

    # Minor ticks
    ax.set_xticks(np.arange(-.5, side, 1), minor=True)
    ax.set_yticks(np.arange(-.5, side, 1), minor=True)

    ax.grid(which='minor', axis='both', linestyle='-', color=hex_to_rgb("#a5b1c2"), linewidth=1)
        
    plt.gca().invert_yaxis()
    plt.gca().set_aspect('equal', adjustable='box')  
    
    if path:
        xs, ys = map(list, zip(*path))
        ax.plot(xs, ys, linestyle="--", color="black")
    
    plt.show()


def show_path(start, end, blocks=[], path=[], attempted=[], side=20, \
    background_colour="#FFF9F0", start_colour="#FC5C65", end_colour="#45AAF2", block_colour="#A5B1C2", attempt_colours=("#FAFF3E", "#3FF5F1")) :
    
    data = [[hex_to_rgb(background_colour)] * side for _ in range(side)]

    for block in blocks:
        x, y = block
        data[y][x] = hex_to_rgb(block_colour)
    
    for attempt in attempted:
        x, y = attempt
        t = progress(start, end, attempt)
        data[y][x] = interpolate(hex_to_rgb(attempt_colours[0]), hex_to_rgb(attempt_colours[1]), t)

    x, y = start
    data[y][x] = hex_to_rgb(start_colour)
    
    x, y = end
    data[y][x] = hex_to_rgb(end_colour)

    show_grid(data, path, side=side)


def show_graph(edges, start=None, end=None, path=None, side=20, \
    background_colour="#FFF9F0", node_colour="#00FF00", start_colour="#FC5C65", end_colour="#45AAF2"):

    data = [[hex_to_rgb(background_colour)] * side for _ in range(side)]

    for edge in edges:
        x, y = edge.pos
        data[y][x] = hex_to_rgb(node_colour)

    if start:
        x, y = start
        data[y][x] = hex_to_rgb(start_colour)
    
    if end:
        x, y = end
        data[y][x] = hex_to_rgb(end_colour)

    show_grid(data, path, side=side)

