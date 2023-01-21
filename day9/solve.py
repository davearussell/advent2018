#! /usr/bin/python3
import sys


def play(n_players, last_marble):
    n_marbles = last_marble + 1
    scores = [0] * n_players
    left = [None] * n_marbles
    right = [None] * n_marbles
    current = 0
    left[current] = current
    right[current] = current

    for marble in range(1, n_marbles):
        if marble % 23 == 0:
            for _ in range(6):
                current = left[current]
            to_remove = left[current]
            l = left[to_remove]
            right[l] = current
            left[current] = l
            scores[marble % n_players] += marble + to_remove
        else:
            l = right[current]
            r = right[l]
            left[marble] = l
            right[marble] = r
            left[r] = marble
            right[l] = marble
            current = marble

    return max(scores)


def main(n_players, last_marble):
    print("Part 1:", play(int(n_players), int(last_marble)))
    print("Part 2:", play(int(n_players), int(last_marble) * 100))


if __name__ == '__main__':
    main(*sys.argv[1:])
