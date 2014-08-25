#!/usr/bin/python

__author__ = 'vilelag'

import os
import argparse


def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='Merges class data from files')
    parser.add_argument('-i', '-in', metavar='<file>', nargs='*',
                        help='Class files to be merged')
    parser.add_argument('-o', '-output', metavar='<file>', default='merge_class_data.txt',
                        help='File where the generated class data will be saved')

    return parser


def save_class(words, fout):
    with open(fout, 'w') as f:
        for word in sorted(words, key=lambda x:x.lower()):
            line = ' '.join(words[word])
            line = '{} {}\n'.format(word, line)
            f.write(line)


def get_words(words, file):
    with open(file, 'r') as f:
        content = f.read().splitlines()

    for line in content:
        tmp = line.split(' ')
        name = tmp[0]
        classes = tmp[1:]
        for _class in classes:
            try:
                if _class not in words[name]:
                    words[name].append(_class)
            except KeyError:
                words[name] = [_class]
    return  words


def main():
    parser = create_parsers()
    args = vars(parser.parse_args())
    fin = args['i']
    fout = args['o']

    if len(fin) < 1:
        exit(1)
    words = dict()
    for file in fin:
        words = get_words(words, file)

    save_class(words, fout)


main()