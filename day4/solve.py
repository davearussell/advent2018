#! /usr/bin/python3
import re
import sys


def parse_input(path):
    pat = re.compile(r"^.(\d+).(\d+).(\d+) (\d+):(\d+). (.+)\n")
    events = []
    for line in open(path):
        fields = pat.match(line).groups()
        ts = [int(x) for x in fields[:5]]
        msg = fields[5]
        if '#' in msg:
            guard = int(msg.split()[1][1:])
            event = (ts, guard, 'start')
        elif 'sleep' in msg:
            event = (ts, None, 'sleep')
        elif 'wake' in msg:
            event = (ts, None, 'wake')
        else:
            assert 0,  repr(line)
        events.append(event)
    events.sort()
    current_guard = None
    for i, (ts, guard, event) in enumerate(events):
        if guard is not None:
            current_guard = guard
        else:
            events[i] = (ts, current_guard, event)
    return events


def track_sleep(events):
    slept = {}
    current_guard = None
    asleep_m = None
    for (_, _, _, _, m), guard, action in events:
        if action == 'start':
            current_guard = guard
            assert asleep_m is None
        elif action == 'sleep':
            assert asleep_m is None
            asleep_m = m
        elif action == 'wake':
            assert asleep_m is not None
            slept.setdefault(current_guard, {})
            for sm in range(asleep_m, m):
                slept[current_guard][sm] = slept[current_guard].get(sm, 0) + 1
            asleep_m = None
    return slept


def main(input_file):
    events = parse_input(input_file)
    slept = track_sleep(events)

    guard1 = max(slept, key = lambda g: sum(slept[g].values()))
    minute1 = max(slept[guard1], key= lambda m: slept[guard1][m])
    print("Part 1:", guard1 * minute1)

    guard2 = max(slept, key = lambda g: max(slept[g].values()))
    minute2 = max(slept[guard2], key= lambda m: slept[guard2][m])
    print("Part 2:", guard2 * minute2, guard2, minute2)


if __name__ == '__main__':
    main(sys.argv[1])
