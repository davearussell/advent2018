#! /usr/bin/python3


# This function is specific to my input and yields the list of R0 values
# that will cause the program to terminate, sorted by increasing runtime
def sequence():
    r1 = r5 = 0
    seen = set()
    values = []
    while True:
        r5 = r1 | 65536
        r1 = 8595037
        while True:
            r1 = (((r1 + (r5 & 255)) & 0xffffff) * 65899) & 0xffffff
            if r5 < 256:
                break
            r5 >>= 8
        if r1 in seen:
            return values
        seen.add(r1)
        values.append(r1)


def main():
    halt_values = sequence()
    print("Part 1:", halt_values[0])
    print("Part 2:", halt_values[-1])


if __name__ == '__main__':
    main()
