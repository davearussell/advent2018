#! /usr/bin/python3
import re
import sys


WET, WATER, CLAY = range(3)
def parse_input(path):
    veins = []
    pat = re.compile(r'([xy])=(\d+), ([xy])=(\d+)[.][.](\d+)')
    for line in open(path).read().strip().split('\n'):
        a, av, b, bv0, bv1 = pat.match(line).groups()
        av, bv0, bv1 = [int(x) for x in [av, bv0, bv1]]
        if a == 'x':
            veins.append(((av, av), (bv0, bv1)))
        else:
            veins.append(((bv0, bv1), (av, av)))
    grid = {}
    for (x0, x1), (y0, y1) in veins:
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                grid[(x, y)] = CLAY
    return grid


def explore(grid, pos, direction):
    x, y = pos
    while True:
        x += direction
        if grid.get((x, y)):
            return False, x - direction
        if not grid.get((x, y + 1)):
            return True, x


def spread(grid, pos):
    x, y = pos
    dropl, xl = explore(grid, pos, -1)
    dropr, xr = explore(grid, pos, 1)
    any_drop = dropl or dropr
    drips = set()
    for _x in range(xl, xr + 1):
        grid[(_x, y)] = WET if any_drop else WATER
    if not any_drop:
        drips.add((x, y - 1))
    if dropl:
        drips.add((xl, y))
    if dropr:
        drips.add((xr, y))
    return drips


def drip(grid, start_pos, maxy):
    drips = {start_pos}
    while drips:
        new_drips = set()
        for drip in drips:
            if grid.get(drip) == WATER:
                new_drips.add((drip[0], drip[1] - 1))
                continue
            while drip[1] < maxy and not grid.get(down := (drip[0], drip[1] + 1)):
                grid[drip := down] = WET
            if drip[1] < maxy:
                new_drips |= spread(grid, drip)
        drips = new_drips


def main(input_file):
    grid = parse_input(input_file)
    miny = min(y for (x, y) in grid)
    maxy = max(y for (x, y) in grid)
    drip(grid, (500, 0), maxy)
    wet = len([0 for (x, y), z in grid.items() if z == WET and miny <= y <= maxy])
    water = len([0 for (x, y), z in grid.items() if z == WATER])
    print("Part 1:", wet + water)
    print("Part 2:", water)


if __name__ == '__main__':
    main(sys.argv[1])
