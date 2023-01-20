#! /usr/bin/python3
import copy
import sys


def parse_input(path):
    spls = [line.split() for line in open(path) if line.strip()]
    deps = [(spl[1], spl[7]) for spl in spls]
    depends_on = {}
    for b, a in deps:
        depends_on.setdefault(a, []).append(b)
        depends_on.setdefault(b, [])
    return depends_on


def perform_steps(depends_on, n_workers):
    depends_on = copy.deepcopy(depends_on)
    t = 0
    order = []
    workers = [(0, None)] * n_workers
    while True:
        ready_workers = []
        for worker, (free_at, step) in enumerate(workers):
            if t >= free_at:
                ready_workers.append(worker)
                if step and t == free_at:
                    order.append(step)
                    for l in depends_on.values():
                        if step in l:
                            l.remove(step)
        if not depends_on and len(ready_workers) == n_workers:
            break
        ready_steps = sorted(k for k, v in depends_on.items() if not v)
        for worker, step in zip(ready_workers, ready_steps):
            del depends_on[step]
            duration = ord(step) - ord('A') + 61
            workers[worker] = (t + duration, step)
        t += 1
    return t, order


def main(input_file):
    depends_on = parse_input(input_file)
    _, order = perform_steps(depends_on, 1)
    print("Part 1:", ''.join(order))
    duration, _ = perform_steps(depends_on, 5)
    print("Part 2:", duration)


if __name__ == '__main__':
    main(sys.argv[1])
