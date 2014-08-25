#!/usr/bin/python
__author__ = 'vilelag'

import os
import argparse
import subprocess
from time import strftime
import numpy as np


def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='Generate configurations to word2vec, run them and save the binaries. '
                                                 'It uses the the same parameters as word2vec, but allowing to make '
                                                 'them vary in a given interval.')
    parser.add_argument('-w2v', metavar='<word2vec_exec>', default='./word2vec/word2vec',
                        help='Path to the word2vec executable')
    parser.add_argument('-train', metavar='<train_file>', default='./word2vec/text8',
                        help='Use text data from <file> to train the model')
    parser.add_argument('-folder', metavar='<out_folder>', default='OutFolder',
                        help='Folder where the log and the outputs will be saved')
    parser.add_argument('-log', metavar='<log>', default='out.csv',
                        help='logfile containing the information about how each output was generated. '
                             'It wil be saved in <out_folder>')
    parser.add_argument('-import', metavar='<log>',
                        help='Logfile containing results of another iteration, when passed "-log" will be ignored')
    parser.add_argument('-output', metavar='<file_name>', default='output',
                        help='Use <file_name+args>.bin to save the resulting word vectors / word clusters')
    parser.add_argument('-tmp', metavar='<file>', default='vocab.tmp')
    parser.add_argument('-size', metavar=('<int>', '<step> <end>'), nargs='+', default=[100], type=int,
                        help='Set size of word vectors; default is 100')
    parser.add_argument('-window', metavar=('<int>', '<step> <end>'), nargs='+', default=[5], type=int,
                        help='Set max skip length between words; default is 5')
    parser.add_argument('-sample', metavar=('<float>', '<step> <end>'), nargs='+', default=[0], type=float,
                        help='Set threshold for occurrence of words. Those that appear with higher frequency'
                             'in the training data will be randomly down-sampled;'
                             ' default is 0 (off), useful value is 1e-5')
    parser.add_argument('-hs', metavar='<int>', nargs='+', default=[1], type=int,
                        help='Use Hierarchical Softmax; default is 1 (0 = not used)')
    parser.add_argument('-negative', metavar=('<int>', '<step> <end>'), nargs='+', default=[0], type=int,
                        help='Number of negative examples; default is 0, common values are 5 - 10 (0 = not used)')
    parser.add_argument('-threads', metavar='<int>', nargs=1, default=[8], type=int,
                        help='Use <int> threads (default 8)')
    parser.add_argument('-min_count','-min-count', metavar=('<int>', '<step> <end>'), nargs='+', default=[5], type=int,
                        help='This will discard words that appear less than <int> times; default is 5')
    parser.add_argument('-alpha', metavar=('<float>', '<step> <end>'), nargs='+', default=[0.025], type=float,
                        help='Set the starting learning rate; default is 0.025')
    parser.add_argument('-classes', metavar='<int>', nargs=1, default=[0], type=int,
                        help='Output word classes rather than word vectors; '
                             'default number of classes is 0 (vectors are written)')
    parser.add_argument('-debug', metavar='<int>', nargs=1, default=[2], type=int,
                        help='Set the debug mode (default = 2)')
    parser.add_argument('-binary', metavar='<int>', nargs=1, default=[1], type=int,
                        help='Save the resulting vectors in binary mode; default is 1 (on)')
    parser.add_argument('-cbow', metavar='<int>', nargs='+', default=[0], type=int,
                        help='Use the continuous bag of words model; default is 0 (skip-gram model)')
    parser.add_argument('-nc', nargs='?', const='1', default=None,
                        help='If present, will calculate the number of cases and exit')
    return parser


def create_output_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def call_word2vec(cmd):
    cmd_call = cmd.split(' ')
    try:
        subprocess.check_call(cmd_call)
        print '\n\n'
    except subprocess.CalledProcessError as e:
        print "{0}\nFAILED! with Return Code: {1}".format(" ".join(e.cmd), e.returncode)


def generate_command(w2v, train, output, size, window, sample, hs, negative, threads, min_count, alpha, classes,
                     debug, binary, save_vocab, read_vocab, cbow):
    if read_vocab is None:
        cmd = '{0} -train {1} -output {2} -size {3} -window {4} -sample {5} -hs {6} -negative {7} -threads {8}' \
            ' -min-count {9} -alpha {10} -classes {11} -debug {12} -binary {13} -save-vocab {14} -cbow {15}'.format(
            w2v, train, output, size, window, sample, hs, negative, threads, min_count, alpha, classes, debug, binary,
            save_vocab, cbow)
    else:
        cmd = '{0} -train {1} -output {2} -size {3} -window {4} -sample {5} -hs {6} -negative {7} -threads {8}' \
            ' -min-count {9} -alpha {10} -classes {11} -debug {12} -binary {13} -read-vocab {14} -cbow {15}'.format(
            w2v, train, output, size, window, sample, hs, negative, threads, min_count, alpha, classes, debug, binary,
            read_vocab, cbow)

    return cmd


def generate_filename(base, info, extension, max_len):
    return base+info.rjust(max_len, '0')+extension


def log_line(output, train, size, window, sample, hs, negative, threads,
             min_count, alpha, classes, debug, binary, cbow):
    return '{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};' \
           '{10};{11};{12};{13};{14};{15}\n'.format(output, strftime("%H:%M:%S"), strftime("%Y-%m-%d"), train, size,
                                                  window, sample, hs, negative, threads, min_count, alpha, classes,
                                                  debug, binary, cbow)


def check_an_arg(arg):
    if len(arg) == 1:
        arg.extend([1, arg[0]+1])
    elif len(arg) > 3:
        del arg[3:]


def check_args(args):
    check_an_arg(args['size'])
    check_an_arg(args['window'])
    check_an_arg(args['sample'])
    check_an_arg(args['hs'])
    check_an_arg(args['negative'])
    check_an_arg(args['min_count'])
    check_an_arg(args['alpha'])
    check_an_arg(args['cbow'])


def create_range(arg):
    return np.arange(arg[0], arg[2], arg[1]).tolist()


def get_max_cases(args):
    return len(create_range(args['size'])) * len(create_range(args['window'])) * len(create_range(args['sample'])) * \
           len(create_range(args['hs'])) *\
           len(create_range(args['negative'])) * len(create_range(args['min_count'])) *\
           len(create_range(args['alpha'])) * len(create_range(args['cbow']))


def import_log(log):
    with open(log) as f:
        content = f.read().splitlines()
    data = dict()
    for i in range(1, len(content)):
        temp = content[i].split(';')
        data[';'.join(temp[3:9]+temp[10:13]+temp[14:16])] = 1
    return data


def main():
    parser = create_parsers()
    args = vars(parser.parse_args())
    create_output_folder(args['folder'])
    check_args(args)
    start_time = strftime("_%Y-%m-%d_%H-%M-%S_")
    w2v = args['w2v']
    train = args['train']
    output = args['folder']+'/'+args['output']+start_time
    threads = args['threads'][0]
    classes = args['classes'][0]
    debug = args['debug'][0]
    binary = args['binary'][0]
    save_vocab = args['tmp']
    read_vocab = None

    past_log = dict()
    if args['import'] is not None:
        past_log = import_log(args['import'])
        log_file = open(args['import'], 'a')
    else:
        log = args['folder']+'//'+args['log']
        log_file = open(log, 'w')
        log_file.write('output;time;date;train;size;window;sample;hs;negative;threads;'
                       'min-count;alpha;classes;debug;binary;cbow'+os.linesep)
    cases = 0
    past_cases = len(past_log)
    flag = 0
    total_cases = get_max_cases(args)
    if args['nc'] is not None:
        print "This command generates {0} cases\n".format(total_cases)
        return 0

    for size in create_range(args['size']):
        for window in create_range(args['window']):
            for sample in create_range(args['sample']):
                for hs in create_range(args['hs']):
                    for negative in create_range(args['negative']):
                        for min_count in create_range(args['min_count']):
                            for alpha in create_range(args['alpha']):
                                for cbow in create_range(args['cbow']):
                                    try:
                                        flag = past_log[';'.join([str(x) for x in [train, size, window, sample, hs,
                                                                                   negative, min_count, alpha,
                                                                                   classes, binary, cbow]])]
                                    except KeyError:
                                        flag = 0
                                    if flag == 0:
                                        t_output = generate_filename(output, str(cases), '.bin', len(str(total_cases)))
                                        if cases == 0:
                                            cmd = generate_command(w2v, train, t_output, size, window, sample, hs, negative,
                                                                   threads, min_count, alpha, classes, debug, binary,
                                                                   save_vocab, read_vocab, cbow)
                                            read_vocab = save_vocab
                                        else:
                                            cmd = generate_command(w2v, train, t_output, size, window, sample, hs, negative,
                                                                   threads, min_count, alpha, classes, debug, binary,
                                                                   save_vocab, read_vocab, cbow)
                                        print '{0}/{1} : {2:.2f}'.format(cases+past_cases, total_cases,
                                                                         100*float(cases+past_cases)/float(total_cases))
                                        print cmd
                                        call_word2vec(cmd)
                                        log_file.write(log_line(t_output, train, size, window, sample, hs, negative, threads,
                                                                min_count, alpha, classes, debug, binary, cbow))
                                        cases += 1

    log_file.close()
    if cases > 0:
        os.remove(save_vocab)

main()