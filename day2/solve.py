#! /usr/bin/python3
import sys


def main(input_file):
    box_ids = open(input_file).read().split()
    twos = threes = 0
    for box_id in box_ids:
        d = {c: box_id.count(c) for c in box_id}
        if 2 in d.values():
            twos += 1
        if 3 in d.values():
            threes += 1
    print("Part 1:", twos * threes)

    for i, a in enumerate(box_ids):
        for b in box_ids[i+1:]:
            l = [i for i in range(len(a)) if a[i] != b[i]]
            if len(l) == 1:
                print("Part 2:", a[:l[0]] + a[l[0]+1:])
        


if __name__ == '__main__':
    main(sys.argv[1])
