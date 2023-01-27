#! /usr/bin/python3
import sys

DIRECTIONS = 'NESW'
OFFSETS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def get_choices(pat):
    assert pat[0] == '('
    pat = pat[1:]
    depth = 1
    choices = ['']
    for i, char in enumerate(pat):
        if char == '|' and depth == 1:
            choices.append('')
        elif char == ')' and depth == 1:
            return choices, pat[i + 1:]
        else:
            choices[-1] += char
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
    assert 0, depth


def make_edges(pat, pos):
    edges = []
    while pat:
        if pat[0] in DIRECTIONS:
            direction = DIRECTIONS.index(pat[0])
            x, y = pos
            dx, dy = OFFSETS[direction]
            new_pos = (x + dx, y + dy)
            edges.append((pos, new_pos))
            pos = new_pos
            pat = pat[1:]
        else:
            choices, pat = get_choices(pat)
            for choice in choices:
                edges += make_edges(choice, pos)
    return edges


def to_dict(edges):
    dedges = {}
    for a, b in edges:
        dedges.setdefault(a, set()).add(b)
        dedges.setdefault(b, set()).add(a)
    return dedges


def path_lengths(edges, start_pos):
    visited = set()
    frontier = {start_pos}
    lengths = []
    while frontier:
        lengths.append(frontier)
        new_frontier = set()
        for pos in frontier:
            new_frontier |= edges[pos]
        visited |= frontier
        frontier = new_frontier - visited
    return lengths


def main(input_file):
    pat = open(input_file).read().strip()
    assert pat[0] == '^' and pat[-1] == '$'
    pat = pat[1:-1]
    start_pos = (0, 0)
    edges = to_dict(make_edges(pat, start_pos))
    lengths = path_lengths(edges, start_pos)
    print("Part 1:", len(lengths) - 1)
    print("Part 2:", sum(map(len, lengths[1000:])))


if __name__ == '__main__':
    main(sys.argv[1])
