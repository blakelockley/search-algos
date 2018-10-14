import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from .drawing import hex_to_rgb

class Node:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos # pos is only used to disaply our graph on a grid
        
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return "Node('%s', pos=%s)" % (self.name, self.pos)


class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.edges = defaultdict(list)

    def add_edge(self, v1, v2, weight):
        self.edges[v1].append((v2, weight))
        
        if not self.directed:
            self.edges[v2].append((v1, weight))
            
    def add_node(self, node):
        """Required only to add nodes without edges."""
        self.edges[node] = []


    def show(self, start=None, end=None, path=[], side=20, \
        background_colour="#FFF9F0", node_colour="#95F99E", start_colour="#FC5C65", end_colour="#45AAF2"):

        # set up image data
        data = [[hex_to_rgb(background_colour)] * side for _ in range(side)]

        for edge in self.edges:
            x, y = edge.pos
            data[y][x] = hex_to_rgb(node_colour)

        if start:
            x, y = start.pos
            data[y][x] = hex_to_rgb(start_colour)
        
        if end:
            x, y = end.pos
            data[y][x] = hex_to_rgb(end_colour)

        # crate grid
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

        try:

            if path:
                path = list(map(lambda n: n.pos, path))
                xs, ys = map(list, zip(*path))
                ax.plot(xs, ys, linestyle="--", color="red")

            # skip all edges in path for clearer drawing
            skip_edges = []
            for i in range(len(path) - 1):
                skip_edges.append((path[i], path[i + 1]))

            for (name, (x, y)) in  map(lambda n: (n.name, n.pos),  self.edges.keys()):
                ax.annotate(name, (x - 0.5, y - 0.5))

            for (key) in self.edges.keys():
                for (edge, w) in self.edges[key]:
                    a, b = key.pos, edge.pos

                    # Set weight label at midpoint
                    ax_, ay, bx, by = a + b
                    cx, cy = (ax_ + bx) / 2, (ay + by ) / 2 + 0.75

                    ax.annotate(str(w), (cx - 0.5, cy - 0.5))

                    if (a, b) in skip_edges or (b, a) in skip_edges:
                        continue

                    ax.annotate("", (bx, by), xytext=(ax_, ay), arrowprops={"arrowstyle": "->" if self.directed else "-", "color": "black"})

        except AttributeError:
            raise AttributeError("Node objects must contain a 'pos' attribute to be displayed.")
                
        plt.gca().invert_yaxis()
        plt.gca().set_aspect('equal', adjustable='box')
        


    