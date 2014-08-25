#!/usr/bin/python
__author__ = 'vilelag'

import os
import argparse
import subprocess
from multiprocessing import Pool
import sys


def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='Run the compute-accuracy test over dictionaries created from word2vec.'
                                                 '\nThis file is out-dated, using genereate_logs.py is preferable.')
    parser.add_argument('-ca', metavar='<compute-accuracy_exec>', default='./word2vec/compute-accuracy',
                        help='Path to the compute-accuracy executable')
    parser.add_argument('-test', metavar='<train_file>', default='./word2vec/questions-words.txt',
                        help='Use text data from <file> to test the model')
    parser .add_argument('-folder', metavar='<folder>', default='./OutFolder',
                         help='Folder where all the dictionaries to be tested are saved')
    parser.add_argument('-threads', metavar='<int>', nargs=1, default=[8], type=int,
                        help='Use <int> threads (default 8)')
    parser.add_argument('-nc', nargs='?', const='1', default=None,
                        help='If present, will calculate the number of cases and exit')
    parser.add_argument('-lf', metavar='<folder>', default='./LogFolder',
                        help='Folder where the logs will be saved')
    parser.add_argument('-p', nargs='?', default=None, const=1,
                        help='If present the process will be persistent, will keep checking "<folder>" until stopped')
    parser.add_argument('-t', metavar='<int>', nargs=1, default=[30000], type=int,
                        help='Threshold is used to reduce vocabulary of the model for fast approximate evaluation '
                             '(0 = off, otherwise typical value is 30000, default=30000)')
    return parser


def create_output_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_file_list(dir):
    fl = []
    for f in os.listdir(dir):
        if f.endswith(".bin"):
            fl.append(dir+'/'+f)
    return fl


def run_ca(file):
    try:
        flag = data[file]
    except KeyError:
        flag = 0
    if flag == 0:
        out = subprocess.check_output([ca, file, threshold], stdin=open(test, 'r'))
        log_f = os.path.splitext(os.path.basename(file))[0]
        log_f = log_folder+'/'+log_f+'.log'
        with open(log_f, "w") as text_file:
            text_file.write(os.path.basename(file)+'\n')
            text_file.write(out)
        print file


def main():
    global data
    global n_dics
    fl = get_file_list(folder)
    n_dics = len(fl)
    if args['nc'] is not None:
        print '{0} dictionaries to test\n'.format(n_dics)
        os.exit(0)

    pool = Pool(threads)
    pool.map(run_ca, fl)

    for file in fl:
        data[file] = 1


parser = create_parsers()
args = vars(parser.parse_args())
data = dict()
max_run = 10000
cur_run = 0
ca = args['ca']
test = args['test']
folder = args['folder']
threads = args['threads'][0]
threshold = str(args['t'][0])
log_folder = args['lf']
create_output_folder(log_folder)
n_dics = int()
if args['p'] is not None:
    while True:
        main()
        cur_run += 1
        if (cur_run%1000) == 0:
            print('Persistent mode: on\n')
        if cur_run >= max_run:
            print 'Max iterations arrived, process exit\n'
            exit(0)
else:
    main()