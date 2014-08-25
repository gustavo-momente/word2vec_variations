#!/usr/bin/python

__author__ = 'vilelag'

import os
import argparse
import numpy as np


def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='Average  results from many rep_dist.py runs. For usage example,'
                                                 ' please, check ./Tests/start_config/ca_nosub/mean.sh')

    parser.add_argument('-f', '-folder', metavar='<folder>', required=True,
                        help='Folder with all the draws to be averaged')
    parser.add_argument('-o', '-out', metavar='<file>', required=True,
                        help='File where the mean log will be saved')

    return parser


def get_files(folder):
    files = ['{0}/{1}'.format(folder, n) for n in os.listdir(folder) if os.path.isfile(os.path.join(folder, n))]
    return files


def read_log(log):
    with open(log) as f:
        content = f.read().splitlines()
    data = dict()
    for case in content[2:]:
        tmp = case.split(' ')
        data[tmp[0].rstrip(':')] = float(tmp[1])
    return data, content[0], content[1]


def save_log(data, l0, l1, out):
    print out
    f = open(out, 'w')
    f.write('{}\n{}\n'.format(l0, l1))
    for _type in sorted(data):
            f.write('{}: {}\n'.format(_type, data[_type]))
    f.close()


def main():
    parser = create_parsers()
    args = vars(parser.parse_args())

    in_folder = args['f'].rstrip('/')
    out = args['o'].rstrip('/')

    # Get draws
    draws = get_files(in_folder)
    cases = len(draws)

    data = dict()
    l0 = ''
    l1 = ''
    for log in draws:
        data[log], l0, l1 = read_log(log)

    mean = dict()

    # calculating mean
    for log in draws:
        for case in data[log]:
            try:
                mean[case] += data[log][case]
            except KeyError:
                mean[case] = data[log][case]

    for key in mean:
        mean[key] /= cases

    # sig2
    sig2 = dict()
    for log in draws:
        for case in data[log]:
            try:
                sig2[case] += (data[log][case] - mean[case]) ** 2
            except KeyError:
                sig2[case] = (data[log][case] - mean[case]) ** 2

    for key in sig2:
        sig2[key] /= cases - 1

    save_log(mean, l0, l1, out)
    save_log(sig2, l0, l1, '{}_sig2'.format(out))

main()