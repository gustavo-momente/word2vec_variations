#!/usr/bin/python
import shutil

__author__ = 'vilelag'

import os
import argparse
import itertools


def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='Creates a pseudo-compute-accuracy test file '
                                                 'based on SemEval-2012 Task2 classes')
    parser.add_argument('-folder', metavar='<folder>', default='./SE2012/Training/Phase1Answers',
                        help='Folder where all the SemEval answers are')
    # parser.add_argument('-threads', metavar='<int>', nargs=1, default=[8], type=int,
    #                     help='Use <int> threads (default 8)')
    parser.add_argument('-out', metavar='<test_file>', default='questions.txt',
                        help='Output file')
    parser.add_argument('-scl', metavar='<scl_file>', default='SE2012/subcategories-list.txt',
                        help='Path to Subcategories-list file')
    return parser


def read_subcategories_list(a_file):
    with open(a_file) as f:
        content = f.read().splitlines()
    subcat = dict()
    for line in content:
        spt = line.split(', ')
        # subcat[''.join(spt[0:2])] = '-'.join(spt[2:]).replace(' ', '-').replace(':','--').replace('/', '|')
        subcat[''.join(spt[0:2])] = '-'.join(spt[2:]).replace(' ', '-').replace('/', '|')
    # for a in sorted(subcat, key= lambda x: int(x[:-1])*27+ord(x[-1].lower())-ord('a')):
    #     print '{} : {}'.format(a, subcat[a])
    return subcat


def get_file_list(dir, ext='.txt'):
    fl = []
    for f in os.listdir(dir):
        if f.endswith(ext):
            fl.append(dir+'/'+f)
    return fl


def get_all_pairs(answers):

    pairs_in_category = dict()
    for ans in answers:
        t_type = ans.split('-')[-1].split('.')[0]
        with open(ans) as f:
            content = f.read().splitlines()
        t_pairs = []
        for pair in content:
            pair = pair.rstrip('"').lstrip('"')
            t_str = pair.split(':')
            flag = 0
            for el in t_str:
                if len(el.split(' ')) != 1:
                    flag = 1
                    print "The element: '{}' in {} has spaces, we won't use it".format(el, ans)
                    break
            if flag == 1:
                continue
            t_pairs.append(' '.join(t_str))
        pairs_in_category[t_type] = t_pairs

    return pairs_in_category


def create_questions_for_nocaw(out, pairs_in_category, subcategories):
    f = open(out, 'w')

    for category in sorted(pairs_in_category, key=lambda x: int(x[:-1])*27+ord(x[-1].lower())-ord('a')):
        # if len(subcategories[category]) < 50:
        #     name = subcategories[category]
        # else:
        #     name = category
        f.write(': {}\n'.format(subcategories[category]))
        for i in range(0, len(pairs_in_category[category]), 2):
            try:
                f.write('{} {}\n'.format(pairs_in_category[category][i], pairs_in_category[category][i+1]))
            except IndexError:
                f.write('{} {}\n'.format(pairs_in_category[category][i], pairs_in_category[category][0]))
    f.close()




def create_questions_for_caw(out, pairs_in_category, subcategories):
    f = open(out, 'w')

    for category in sorted(pairs_in_category, key=lambda x: int(x[:-1])*27+ord(x[-1].lower())-ord('a')):
        f.write(': {}\n'.format(subcategories[category]))
        combinations = itertools.combinations(pairs_in_category[category], 2)

        for c in combinations:
            f.write('{} {}\n'.format(c[0], c[1]))

    f.close()


def main():
    parser = create_parsers()
    args = vars(parser.parse_args())

    folder = args['folder']
    out = args['out']
    scl = args['scl']

    subcategories = read_subcategories_list(scl)
    answers = get_file_list(folder)
    pairs_in_category = get_all_pairs(answers)

    f = open(out, 'w')

    # create_questions_for_nocaw(out, pairs_in_category, subcategories)
    create_questions_for_caw(out, pairs_in_category, subcategories)

main()