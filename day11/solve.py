#! /usr/bin/python3
import sys

import numba
import numpy


@numba.njit(cache=True)
def power_level(x, y, serial):
    rack = x + 10
    power = rack * y
    power += serial
    power *= rack
    return (power // 100) % 10 - 5


@numba.njit(cache=True)
def choose_square(grid_size, serial, minsize, maxsize):
    grid = numpy.zeros((grid_size + 1, grid_size + 1), dtype=numpy.int8)
    for x in range(1, grid_size + 1):
        for y in range(1, grid_size + 1):
            grid[x][y] = power_level(x, y, serial)

    best = (0, 0, 0, None)
    for c in range(minsize, maxsize + 1):
        cbest = None
        for x in range(1, grid_size + 2 - c):
            for y in range(1, grid_size + 2 - c):
                v = numpy.sum(grid[x:x+c,y:y+c])
                if cbest is None or v > cbest:
                    cbest = v
                if best[3] is None or v > best[3]:
                    best = (x, y, c, v)
        if cbest < 0:
            break

    return best[0], best[1], best[2]


def main(serial):
    print("Part 1:", choose_square(300, serial, 3, 3))
    print("Part 1:", choose_square(300, serial, 1, 300))


if __name__ == '__main__':
    main(int(sys.argv[1]))
