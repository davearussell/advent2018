#! /usr/bin/python3
import sys

DIRECTIONS = '^>v<'
FORWARD = {1: (1, 0), 3: (-1, 0), 0: (0, -1), 2: (0, 1)}


def parse_input(path):
    data = open(path).read().rstrip('\n')
    grid = [list(row) for row in data.split('\n')]
    carts = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in DIRECTIONS:
                carts[(x, y)] = (DIRECTIONS.index(cell), 0)
                grid[y][x] = '-' if cell in '<>' else '|'
    return grid, carts


def tick(grid, carts):
    new_carts = {}
    crashes = []
    for (x, y) in sorted(carts):
        if (x, y) not in carts:
            continue
        direction, state = carts.pop((x, y))
        dx, dy = FORWARD[direction]
        x, y = (x + dx, y + dy)
        if (x, y) in carts or (x, y) in new_carts:
            carts.pop((x, y), None)
            new_carts.pop((x, y), None)
            crashes.append((x, y))
            continue
        if grid[y][x] == '+':
            if state in (0, 2):
                direction = (direction + state - 1) % len(DIRECTIONS)
            state = (state + 1) % 3
        elif grid[y][x] == '\\':
            direction = 3 - direction
        elif grid[y][x] == '/':
            direction ^= 1
        new_carts[(x, y)] = (direction, state)
    return new_carts, crashes


def main(input_file):
    grid, carts = parse_input(input_file)
    any_crashed = False
    while True:
        carts, crashes = tick(grid, carts)
        if crashes and not any_crashed:
            print("Part 1:", crashes[0])
            any_crashed = True
        if len(carts) == 1:
            print("Part 2:", list(carts)[0])
            break


if __name__ == '__main__':
    main(sys.argv[1])
