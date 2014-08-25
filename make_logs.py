#!/usr/bin/python
__author__ = 'vilelag'

import os
import argparse
import subprocess
from time import strftime
import numpy as np
import math


def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='Generate configurations to word2vec,run it and save the binaries,'
                                                 'then evaluate the binaries and ')
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
    # parser.add_argument('-binary', metavar='<int>', nargs=1, default=[1], type=int,
    #                     help='Save the resulting vectors in binary mode; default is 1 (on)')
    parser.add_argument('-cbow', metavar='<int>', nargs='+', default=[0], type=int,
                        help='Use the continuous bag of words model; default is 0 (skip-gram model)')
    parser.add_argument('-nc', nargs='?', const='1', default=None,
                        help='If present, will calculate the number of cases and exit')
    parser.add_argument('-ca', metavar='<compute-accuracy_exec>', default='./word2vec/compute-accuracy',
                        help='Path to the compute-accuracy executable')
    parser.add_argument('-test', metavar='<train_file>', default='./word2vec/questions-words.txt',
                        help='Use text data from <file> to test the model')
    parser.add_argument('-lf', metavar='<folder>', default='./LogFolder',
                        help='Folder where the ca logs will be saved')
    parser.add_argument('-rd', metavar='run_dics.py', default='./run_dics.py',
                        help='Path to run_dics.py')
    parser.add_argument('-set', metavar='<SE-Test1.py>', default=None,
                        help='Path to SE-Test1.py if present will run it instead of compute-accuracy')
    parser.add_argument('-q', '-questions', metavar='<folder>', default='./SE2012/Testing/Phase1Questions',
                        help='Folder with Phase 1 Questions (SE-Test1.py mode)')
    parser.add_argument('-a', '-answers ', metavar='<folder>', default='./SE2012/Testing/Phase1Answers',
                        help='Folder with Phase 1 Answers (SE-Test1.py mode)')
    parser.add_argument('-SE', metavar='<folder>', default='./SE2012',
                        help='Folder with SE2012 files (SE-Test1.py mode)')
    parser.add_argument('-a2', '-answers2', metavar='<folder>', default='./SE2012/Testing/Phase2Answers',
                        help='Folder with Phase 2 Answers (SE-Test1.py mode)')
    parser.add_argument('-gn', metavar='<generate_net.py>',
                        help='Path to generate_net.py, used when a starting net configuration should be passed '
                             'to word2vec, so when it\'s used word2vec-g should be passed with -w2v')
    parser.add_argument('-c', metavar='<file>', default='class_data.txt',
                        help='Class data that will be passed to generate_net.py')

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


def gen_net(cmd):
    call_word2vec(cmd)


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
    print "Importing log"
    with open(log) as f:
        content = f.read().splitlines()
    data = dict()
    for i in range(1, len(content)):
        temp = content[i].split(';')
        data[';'.join(temp[3:9]+temp[10:13]+temp[14:16])] = 1
    print data
    return data


def run_dics(rd, ca, test, test_folder, threads, log_folder, threshold):
    cmd = '{0} -ca {1} -test {2} -folder {3} -threads {4} -lf {5} -t {6}'.format(rd, ca, test, test_folder,
                                                                                           threads, log_folder,
                                                                                           threshold)
    print cmd
    cmd_call = cmd.split(' ')
    try:
        subprocess.check_call(cmd_call)
        print '\n\n'
    except subprocess.CalledProcessError as e:
        print "{0}\nFAILED! with Return Code: {1}".format(" ".join(e.cmd), e.returncode)


def remove_files(dir):
    fl = []
    for f in os.listdir(dir):
        if f.endswith(".bin"):
            fl.append(dir+'/'+f)
    print "Removing {0} temp files".format(len(fl))
    for file in fl:
        os.remove(file)


def run_se_test1(se_test1, words, questions, answers, out, threads, threshold, se_folde, answers2):
    cmd = '{0} -w {1} -q {2} -a {3} -o {4} -t {5} -threshold {6} -SE {7} -a2 {8}'.format(se_test1, words, questions,
                                                                                      answers, out, threads,
                                                                                         threshold, se_folde, answers2)
    print cmd
    cmd = cmd.split(' ')
    try:
        subprocess.check_call(cmd)
        print '\n'
    except subprocess.CalledProcessError as e:
        print "{0}\nFAILED! with Return Code: {1}".format(" ".join(e.cmd), e.returncode)


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
    # binary = args['binary'][0]
    save_vocab = args['tmp']
    read_vocab = None

    ca = args['ca']
    test = args['test']
    log_folder = args['lf']

    #SE-Test1 args
    se_exec = args['set']
    questions = args['q'].rstrip('/')
    answers = args['a'].rstrip('/')
    answers2 = args['a2'].rstrip('/')
    se_folder = args['SE'].rstrip('/')

    #generate_net args
    gn = args['gn']
    _class = args['c']
    net = 'tmp_net'

    binary = 1
    if se_exec is not None:
        binary = 0

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

    #Creates the vocabulary used by gn if need be
    if gn is not None:
        call_word2vec('{} -train {} -save-vocab {}'.format(w2v, train, save_vocab))

    for size in create_range(args['size']):
        if gn is not None:
            print '{} -v {} -c {} -s {} -o {}'.format(gn, save_vocab, _class, size, net)
            gen_net('{} -v {} -c {} -s {} -o {}'.format(gn, save_vocab, _class, size, net))
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
                                        if gn is not None:
                                            cmd = '{} -load {}'.format(cmd, net)
                                        print cmd
                                        call_word2vec(cmd)
                                        log_file.write(log_line(t_output, train, size, window, sample, hs, negative, threads,
                                                                min_count, alpha, classes, debug, binary, cbow))

                                        if se_exec is None:
                                            if cases+1 % threads == 0:
                                                run_dics(args['rd'], ca, test, args['folder'], threads, log_folder, 0)
                                                # run_dics(args['rd'], ca, test, args['folder'], threads, log_folder+"/30000", 30000)
                                                remove_files(args['folder'])
                                        else:
                                            run_se_test1(se_exec, t_output, questions, answers, args['folder']+'/SE-2012'
                                                                                                               '/{}'.format(
                                                cases), int(math.floor(threads/2)), 0, se_folder, answers2)
                                            remove_files(args['folder'])
                                        cases += 1
        if gn is not None:
            os.remove(net)



    log_file.close()

    if cases > 0 and se_exec is None:
        run_dics(args['rd'], ca, test, args['folder'], threads, log_folder, 0)
        # run_dics(args['rd'], ca, test, args['folder'], threads, log_folder+"/30000", 30000)
        remove_files(args['folder'])
    if cases > 0:
        os.remove(save_vocab)

main()