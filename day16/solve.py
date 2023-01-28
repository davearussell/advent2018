#! /usr/bin/python3
import json
import os
import sys
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import cpu


def parse_input(path):
    data = open(path).read()
    sample_text, prog_text = data.split('\n\n\n\n')
    samples = []
    for sample in sample_text.split('\n\n'):
        lines = sample.split('\n')
        samples.append({
            'before': json.loads(lines[0].split(':')[1]),
            'insn': [int(x) for x in lines[1].split()],
            'after': json.loads(lines[2].split(':')[1]),
        })
    prog = [[int(x) for x in line.split()] for line in prog_text.split('\n') if line.strip()]
    return samples, prog


def main(input_file):
    samples, prog = parse_input(input_file)

    p1_count = 0
    candidates = {}
    for i, sample in enumerate(samples):
        opcode, a, b, c = sample['insn']
        matches = {name for (name, op) in cpu.OPS.items()
                   if op(sample['before'], a, b, c) == sample['after']}
        if len(matches) >= 3:
            p1_count += 1
        if opcode not in candidates:
            candidates[opcode] = matches
        candidates[opcode] &= matches
    print("Part 1:", p1_count)

    op_names = {}
    while candidates:
        for opcode, names in candidates.items():
            if len(names) == 1:
                del candidates[opcode]
                name = names.pop()
                op_names[opcode] = name
                for _names in candidates.values():
                    _names -= {name}
                break

    insns = [(op_names[opcode], (a, b, c)) for (opcode, a, b, c) in prog]
    print("Part 2:", cpu.run(insns)[0])


if __name__ == '__main__':
    main(sys.argv[1])
