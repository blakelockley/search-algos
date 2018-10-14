import numpy as np
import matplotlib.pyplot as plt
from .drawing import hex_to_rgb, interpolate, progress


class Grid:

    def __init__(self, heuristic_func, cost_func, barriers=[], side=20):
        self.heuristic_func = heuristic_func
        self.cost_func = cost_func
        self.barriers = barriers
        self.side = side

    def h(self, a, b):
        return self.heuristic_func(a, b)

    def g(self, a, b):
        return self.cost_func(a, b, self.barriers)

    def neighbours(self, cell):

        offsets = [(-1,  1), (0,  1), (1,  1), \
                   (-1,  0),          (1,  0), \
                   (-1, -1), (0, -1), (1, -1)]

        for (dx, dy) in offsets:
            x, y = cell
            x2, y2 = x + dx, y + dy
            if 0 <= x2 < self.side and 0 <= y2 < self.side:
                yield (x2, y2)

    def show(self, start, end, path=[], attempts=[], \
        background_colour="#FFF9F0", start_colour="#FC5C65", end_colour="#45AAF2", block_colour="#A5B1C2", attempt_colours=("#FAFF3E", "#3FF5F1")):

        # create image data
        data = [[hex_to_rgb(background_colour)] * self.side for _ in range(self.side)]

        for block in self.barriers:
            x, y = block
            data[y][x] = hex_to_rgb(block_colour)
        
        for attempt in attempts:
            x, y = attempt
            t = max(min(self.h(attempt, end) / self.h(start, end), 1), 0) 
            data[y][x] = interpolate(hex_to_rgb(attempt_colours[0]), hex_to_rgb(attempt_colours[1]), t)

        x, y = start
        data[y][x] = hex_to_rgb(start_colour)
        
        x, y = end
        data[y][x] = hex_to_rgb(end_colour)

        _, ax = plt.subplots(figsize=(20, 10))

        ax.imshow(data)
        
        # Major ticks
        ax.set_xticks(np.arange(self.side))
        ax.set_yticks(np.arange(self.side))

        # Labels for major ticks
        ax.set_xticklabels(np.arange(self.side))
        ax.set_yticklabels(np.arange(self.side))

        # Minor ticks
        ax.set_xticks(np.arange(-.5, self.side, 1), minor=True)
        ax.set_yticks(np.arange(-.5, self.side, 1), minor=True)

        ax.grid(which='minor', axis='both', linestyle='-', color=hex_to_rgb("#a5b1c2"), linewidth=1)

        if path:
            xs, ys = map(list, zip(*path))
            ax.plot(xs, ys, linestyle="--", color="black")

        plt.gca().invert_yaxis()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
    


