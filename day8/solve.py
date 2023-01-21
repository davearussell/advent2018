#! /usr/bin/python3
import sys


class Node:
    def __init__(self, values):
        self.children = []
        self.metadata = []
        n_children = values.pop(0)
        n_meta = values.pop(0)
        for i in range(n_children):
            self.children.append(Node(values))
        for i in range(n_meta):
            self.metadata.append(values.pop(0))

        self.part1 = sum(self.metadata) + sum(c.part1 for c in self.children)
        if not self.children:
            self.part2 = self.part1
        else:
            self.part2 = 0
            for v in self.metadata:
                if 1 <= v <= len(self.children):
                    self.part2 += self.children[v - 1].part2


def main(input_file):
    root = Node([int(x) for x in open(input_file).read().split()])
    print("Part 1:", root.part1)
    print("Part 2:", root.part2)


if __name__ == '__main__':
    main(sys.argv[1])
