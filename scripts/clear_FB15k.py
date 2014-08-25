#!/usr/bin/python
__author__ = 'vilelag'

import os
import argparse
import subprocess
from multiprocessing import Pool
import itertools


def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='Convert a tab separated test files to a space separated one.')
    parser.add_argument('-i', '-input', metavar='<file>', required=True,
                        help='Input file in FB15k format')
    # parser.add_argument('-threads', metavar='<int>', nargs=1, default=[8], type=int,
    #                     help='Use <int> threads (default 8)')
    parser.add_argument('-o', '-output', metavar='<file>', default='output.txt',
                        help='Output file with tabs converted to spaces')
    return parser


def convert_file(ipath, opath):
    o = open(opath, 'w')
    with open(ipath) as f:
        for line in f:
            o.write(line.replace('\t', ' '))
    o.close()


def main():
    parser = create_parsers()
    args = vars(parser.parse_args())
    in_f = args['i']
    out_f = args['o']
    convert_file(in_f, out_f)


main()