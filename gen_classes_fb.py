#!/usr/bin/python
__author__ = 'vilelag'

import argparse
import itertools


def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='Create test files based on the fb15k data')
    parser.add_argument('-i', '-input', metavar='<file>', required=True,
                        help='Input file in FB15k format')
    # parser.add_argument('-threads', metavar='<int>', nargs=1, default=[8], type=int,
    #                     help='Use <int> threads (default 8)')
    parser.add_argument('-o', '-output', metavar='<file>', default='questions.txt',
                        help='Output test file')
    parser.add_argument('-n', '-nocaw', metavar='<int>', nargs='?', const=1, default=0,
                        help='If present creates output for no-caw (0: caw, else: no-caw, default: no-caw)')
    return parser


def join_classes(path):
    with open(path) as f:
        content = f.read().splitlines()
    data = dict()
    for line in content:
        tmp = line.split(' ')
        if len(tmp) != 3:
            continue
        t_class = tmp[1]
        try:
            data[t_class].append(tmp[0]+' '+tmp[2])
        except KeyError:
            data[t_class] = [tmp[0]+' '+tmp[2]]

    return data


def create_questions_for_nocaw(out, pairs_in_category):
    f = open(out, 'w')

    for category in sorted(pairs_in_category):
        f.write(': {}\n'.format(category))
        flag = 0
        for i in range(0, len(pairs_in_category[category]), 2):
            flag = 1
            try:
                f.write('{} {}\n'.format(pairs_in_category[category][i], pairs_in_category[category][i+1]))
            except IndexError:
                f.write('{} {}\n'.format(pairs_in_category[category][i], pairs_in_category[category][0]))

        if len(pairs_in_category[category]) == 1 and flag == 0:
            print pairs_in_category[category]
            f.write('{} {}\n'.format(pairs_in_category[category][0], pairs_in_category[category][0]))
    f.close()


def create_questions_for_caw(out, pairs_in_category):
    f = open(out, 'w')

    for category in sorted(pairs_in_category):
        f.write(': {}\n'.format(category))
        combinations = itertools.combinations(pairs_in_category[category], 2)

        for c in combinations:
            f.write('{} {}\n'.format(c[0], c[1]))

    f.close()


def main():
    parser = create_parsers()
    args = vars(parser.parse_args())

    input_f = args['i']
    out = args['o']
    nocaw = args['n']
    pairs_in_category = join_classes(input_f)

    if nocaw  != 0:
        create_questions_for_nocaw(out, pairs_in_category)
    else:
        create_questions_for_caw(out, pairs_in_category)


main()