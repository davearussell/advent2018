#! /usr/bin/python3
import sys


OPEN, TREE, YARD = range(3)
CELLS = {'.': OPEN, '|': TREE, '#': YARD}
SYMBOLS = {v: k for (k, v) in CELLS.items()}
def parse_input(path):
    data = open(path).read().strip()
    grid = {}
    for y, line in enumerate(data.split('\n')):
        for x, c in enumerate(line):
            grid[(x, y)] = CELLS[c]
    return grid, len(line)


def to_str(grid, size):
    s = ''
    for y in range(size):
        for x in range(size):
            s += SYMBOLS[grid[(x, y)]]
        s += '\n'
    return s


def iterate(grid):
    new_grid = {}
    for (x, y), c in grid.items():
        neighbours = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                      (x - 1, y), (x + 1, y),
                      (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        cells = [grid.get(n) for n in neighbours if n in grid]
        if c == OPEN:
            new_grid[(x, y)] = TREE if cells.count(TREE) >= 3 else OPEN
        elif c == TREE:
            new_grid[(x, y)] = YARD if cells.count(YARD) >= 3 else TREE
        elif c == YARD:
            new_grid[(x, y)] = YARD if YARD in cells and TREE in cells else OPEN
    return new_grid


def main(input_file):
    grid, size = parse_input(input_file)

    history = []
    states = {}
    i = 0
    while True:
        s = to_str(grid, size)
        if i == 10:
            print("Part 1:", s.count(SYMBOLS[TREE]) * s.count(SYMBOLS[YARD]))
        if s in states:
            break
        states[s] = i
        history.append(s)
        grid = iterate(grid)
        i += 1

    t0 = states[s]
    offset = (1000000000 - t0) % (i - t0)
    s = history[t0 + offset]
    print("Part 2:", s.count(SYMBOLS[TREE]) * s.count(SYMBOLS[YARD]))


if __name__ == '__main__':
    main(sys.argv[1])
