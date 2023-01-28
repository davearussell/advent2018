#! /usr/bin/python3
import re
import sys

import numpy


def parse_input(path):
    pat = re.compile('depth: (\d+)\ntarget: (\d+),(\d+)')
    values = [int(x) for x in pat.match(open(path).read()).groups()]
    return values[0], (values[1], values[2])


X = 16807
Y = 48271
M = 20183
def get_region_types(target, depth, extend=0):
    xlen = target[0] + 1 + extend
    ylen = target[1] + 1 + extend
    grid = numpy.zeros((xlen, ylen), dtype=numpy.uint64)
    for x in range(xlen):
        for y in range(ylen):
            if (x, y) == target:
                grid[x, y] = depth % M
            elif x == 0:
                grid[x, y] = (Y * y + depth) % M
            elif y == 0:
                grid[x, y] = (X * x + depth) % M
            else:
                grid[x, y] = (grid[x - 1, y] * grid[x, y - 1] + depth) % M
    return grid % 3


def shortest_path(region_types, start, goal):
    mx, my = region_types.shape
    costs = {start: 0}
    steps = {}
    frontier = [(0, start)]

    while frontier:
        frontier.sort()
        cost, pos = frontier.pop(0)
        x, y, tool = pos
        region = int(region_types[x, y])
        neighbours = [(cost + 7, (x, y, 3 - tool - region))]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            n_x, n_y = x + dx, y + dy
            if not (0 <= n_x < mx and 0 <= n_y < my):
                continue
            n_region = region_types[n_x, n_y]
            if n_region != tool:
                neighbours.append((cost + 1, (n_x, n_y, tool)))
        for (n_cost, neighbour) in neighbours:
            if neighbour not in costs or costs[neighbour] > n_cost:
                frontier.append((n_cost, neighbour))
                costs[neighbour] = n_cost
                steps[neighbour] = pos

    return costs.get(goal)


def main(input_file):
    depth, target = parse_input(input_file)
    x, y = target

    region_types = get_region_types(target, depth)
    print("Part 1:", numpy.sum(region_types))

    start = (0, 0, 1)
    goal = (x, y, 1)
    naive_cost = shortest_path(region_types, start, goal)
    lower_bound = x + y
    extra_steps = naive_cost - lower_bound
    extended = get_region_types(target, depth, (extra_steps + 1) // 2)
    print("Part 2:", shortest_path(extended, start, goal))


if __name__ == '__main__':
    main(sys.argv[1])
