#!/usr/bin/python

__author__ = 'vilelag'

import os
import argparse
import re

def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='Generates class data from test file')
    parser.add_argument('-i', '-in', metavar='<file>',
                        help='compute-accuracy test file from where classes will be extracted')
    parser.add_argument('-o', '-output', metavar='<file>', default='class_data.txt',
                        help='File where the generated class data will be saved')
    parser.add_argument('-se', metavar='<int>', nargs='?', const=1, default=0,
                        help='If present will consider the argument passed by -f to generate class data, '
                             '(0: use -i, 1: use -f, default: 0)')
    parser.add_argument('-f', '-folder', metavar='<folder>', default='SE2012/Testing/Phase1Questions',
                        help='Folder with SE-2012 questions')

    return parser


def read_test(fin):
    with open(fin, 'r') as f:
        content = f.read().splitlines()
    words = dict()
    current_class = ''
    inv_class = ''

    for line in content:
        tmp = line.split(' ')
        if len(tmp) == 2:
            current_class = tmp[1]
            inv_class = '{}_h'.format(current_class)
        else:
            for word in tmp[0::2]:
                try:
                    if current_class not in words[word]:
                        words[word].append(current_class)
                except KeyError:
                    words[word] = [current_class]
            for word in tmp[1::2]:
                try:
                    if inv_class not in words[word]:
                        words[word].append(inv_class)
                except KeyError:
                    words[word] = [inv_class]


    return words


def save_class(words, fout):
    with open(fout, 'w') as f:
        for word in sorted(words, key=lambda x:x.lower()):
            line = ' '.join(words[word])
            line = '{} {}\n'.format(word, line)
            f.write(line)


def get_files(folder):
    files = ['{0}/{1}'.format(folder, n) for n in os.listdir(folder) if os.path.isfile(os.path.join(folder, n)) and n.endswith('.txt')]
    return files


def get_class_base(question_f):
    with open(question_f) as f:
        content = f.read().splitlines()
    base = []
    for i in range(4, 7):
        base.append(content[i].split(':'))
    return base


def join_subclasses(files):
    classes = dict()
    for file in files:
        _name = file.split('-')[-1]
        _name = _name.rstrip('.txt')
        _name = re.findall(r'\d+', _name)[0]
        try:
            classes[_name].append(file)
        except KeyError:
            classes[_name] = [file]

    return classes


def read_sub_class(fin, _class, words):
    elements = get_class_base(fin)

    inv_class = "{}_h".format(_class)
    for pair in elements:
        try:
            if _class not in words[pair[0]]:
                words[pair[0]].append(_class)
        except KeyError:
            words[pair[0]] = [_class]

        try:
            if inv_class not in words[pair[1]]:
                words[pair[1]].append(inv_class)
        except KeyError:
            words[pair[1]] = [inv_class]

    return words

def read_se(folder):
    files = get_files(folder)
    _classes = join_subclasses(files)
    words = dict()
    for _class in _classes:
        for sub_class in _classes[_class]:
            words = read_sub_class(sub_class, _class, words)

    return words

def main():
    parser = create_parsers()
    args = vars(parser.parse_args())
    fin = args['i']
    fout = args['o']
    folder = args['f']
    se = args['se']

    if se != 1:
        words = read_test(fin)
    else:
        words = read_se(folder)

    save_class(words, fout)


main()