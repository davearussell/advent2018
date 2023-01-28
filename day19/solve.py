#! /usr/bin/python3
import os
import sys
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import cpu


def factors(n):
    for i in range(1, int(n ** .5) + 1):
        if n % i == 0:
            yield i
            yield n // i


def main(input_file):
    insns, ip = cpu.parse_prog(input_file)

    # Analysing the program revealed it boiled down to:
    # R4 = <big number>
    # for a in range(1, R4 + 1):
    #   for b in range(1, R4 + 1):
    #     if a * b == R4:
    #       R0 += a
    # So we can just run it until it has finished calculating R4
    # and then calculate the sum of factors more efficiently
    insns[1] = ('seti', (1000, 0, ip))

    print("Part 1:", sum(factors(cpu.run(insns, ip_reg=ip)[4])))
    print("Part 2:", sum(factors(cpu.run(insns, state=[1, 0, 0, 0, 0, 0], ip_reg=ip)[4])))


if __name__ == '__main__':
    main(sys.argv[1])
