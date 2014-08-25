#!/usr/bin/python
__author__ = 'vilelag'

import os
import argparse
import subprocess
from time import strftime
import numpy as np
import struct

def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='Computes accuracy of word representations.')
    parser.add_argument("file", metavar='<file.bin>',
                        help='Contains word projections not in binary form')
    parser.add_argument('-threshold', metavar='<int>', default=0, type=int,
                        help="Used to reduce vocabulary of the model for fast approximate evaluation"
                             " (0 = off, otherwise typical values is 30000)")
    return parser


def read_file(path, threshold):
    with open(path) as f:
        content = f.read().splitlines()
    data = dict()
    words, size = content[0].split(' ')
    if 0 < threshold < words:
        words = threshold

    for i in range(1, words+1):
        temp = content[i].split(' ')
        data[temp[0].upper()] = np.asarray([np.float64(x) for x in temp[1:-1]], dtype=np.float64)
        # Normalizing
        data[temp[0].upper()] *= 1 / np.linalg.norm(data[temp[0].upper()])

    return data


def main():
    np.seterr(invalid='ignore')
    parser = create_parsers()
    args = vars(parser.parse_args())
    bin_file = args['file']
    threshold = args['threshold']
    data = read_file(bin_file, threshold)
    tcn = 0
    ccn = 0
    qid = 0
    cacn = 0
    tacn = 0
    seac = 0
    secn = 0
    syac = 0
    sycn = 0
    tq = 0
    tqs = 0
    while True:
        best_dist = 0
        best_word = ''
        try:
            r_l = raw_input().upper().split(" ")
        except EOFError:
            if tcn == 0:
                tcn = 1
            if qid != 0:
                print 'ACCURACY TOP1: {0:.2f} %  ({1} / {2})'.format(ccn/float(tcn)*100, ccn, tcn)
                print 'Total accuracy: {0:.2f} %   Semantic accuracy: {1:.2f} %   Syntactic accuracy: {2:.2f} % ' \
                      ''.format(np.float64(float(cacn))/float(tacn)*100, np.float64(float(seac)) / float(secn)*100, np.float64(float(syac)) / float(sycn)*100)
            break

        if r_l[0] == ':' or r_l[0] == 'EXIT':
            if tcn == 0:
                tcn = 1
            if qid != 0:
                print 'ACCURACY TOP1: {0:.2} %  ({1} / {2})'.format(ccn/float(tcn)*100, ccn, tcn)
                print 'Total accuracy: {0:.2f} %   Semantic accuracy: {1:.2f} %   Syntactic accuracy: {2:.2f} % ' \
                      ''.format(np.float64(float(cacn))/float(tacn)*100, np.float64(float(seac)) / float(secn)*100, np.float64(float(syac)) / float(sycn)*100)
            qid += 1
            if r_l[0] != 'EXIT':
                print "{0}:".format(r_l[1])
            tcn = 0
            ccn = 0
            continue

        if r_l[0] == 'EXIT':
            break

        tq += 1
        try:
            vec = data[r_l[1]] - data[r_l[0]] + data[r_l[2]]
            garbage = data[r_l[3]]
        except KeyError:
            continue

        tqs += 1
        for word, val in data.iteritems():
            if word == r_l[0] or word == r_l[1] or word == r_l[2]:
                continue
            dist = np.dot(vec, val)

            if dist > best_dist:
                best_dist = dist
                best_word = word
        # print '{0:.6f}'.format(dist)
        if best_word == r_l[3]:
            # print "{0:>12} | {1:>12} {2:>12} {3:>12} {4:>12}".format(best_word, r_l[0], r_l[1], r_l[2], r_l[3])
            ccn += 1
            cacn += 1
            if qid <= 5:
                seac += 1
            else:
                syac += 1
        if qid <= 5:
            secn += 1
        else:
            sycn += 1
        tcn += 1
        tacn += 1
        del vec
    print 'Questions seen / total: {0} {1}   {2:.2} % '.format(tqs, tq, tqs/float(tq)*100)


main()


