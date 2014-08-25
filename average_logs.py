#!/usr/bin/python

__author__ = 'vilelag'

import os
import argparse
import numpy as np


def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='Average log results from many files with the same run configuration'
                                                 'for examples check ./Tests/var*/run_all.sh')

    parser.add_argument('-se', metavar='<int>', nargs='?', default=0, const=1, type=int,
                        help='Must be present to use logs generated using "SE-Test1.py" (1 : On, else: Off,'
                             ' Default: Off)')
    parser.add_argument('-f', '-folder', metavar='<folder>', required=True,
                        help='Folder with all the draws to be averaged')
    parser.add_argument('-o', '-o', metavar='<folder>', required=True,
                        help='Folder where the mean logs will be saved')
    parser.add_argument('-csv', metavar='<file>', required=True,
                        help='csv with the configurations to generate a draw')
    parser.add_argument('-ocsv', metavar='<file>', required=True,
                        help='Output csv, basically a copy of <csv> with fixed names')
    return parser


def get_sub_dir(folder, flag=1):
    if flag == 1:
        sub = ['{0}/{1}'.format(folder, n) for n in os.listdir(folder) if os.path.isdir(os.path.join(folder, n))]
    else:
        sub = ['{0}'.format(n) for n in os.listdir(folder) if os.path.isdir(os.path.join(folder, n))]
    sub = sorted(sub)
    return sub


def read_se_log(log):
    with open(log) as f:
        content = f.read().splitlines()
    data = dict()
    for case in content[1:]:
        tmp = case.split(',')
        data[tmp[0]] = float(tmp[1])
    return data


def create_output_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_se_logs(data, out):
    for key in data:
        out_folder = '{}/{}'.format(out, key)
        create_output_folder(out_folder)
        save_se_log(data[key], '{}/log.csv'.format(out_folder))


def fake_csv(csv, csv_o):
    with open(csv, 'r') as f:
        content = f.read().splitlines()

    with open(csv_o, 'w') as o:
        o.write('{}\n'.format(content[0]))
        for i in range(1, len(content)):
            tmp = content[i].split(';')
            # name = os.path.splitext(os.path.basename(tmp[0]))[0]
            name = os.path.basename(tmp[0])
            name = name.split('_')[-1]
            name = 'mean_{}'.format(name)
            tmp[0] = name
            line = ';'.join(tmp)
            o.write('{}\n'.format(line))


def save_sa_logs(data, out):
    for key in data:
        out_name = '{}/mean_{}.log'.format(out,key)
        save_sa_log(data[key], out_name)


def save_se_log(data, out):
    print out
    f = open(out, 'w')
    score = dict()
    f.write('Subcategories,Spearman\n')
    for _type in sorted(data, key=sort_func):
            f.write('{},{}\n'.format(_type, data[_type]))
    f.close()


def save_sa_log(data, out):
    f = open(out, 'w')
    f.write('Class,top1,ta,sem,syn\n')
    for i in sorted(data):
        f.write('{}'.format(i))
        for a in data[i]:
            f.write(',{}'.format(a))
        f.write('\n')
    f.close()


def sort_func(x):
    try:
        num = int(''.join([s for s in x if s.isdigit()]))
        char = x.lstrip(str(num))
        return num*27+ord(char.lower())-ord('a')
    except:
        return 10000


def read_log(log):
    with open(log) as f:
        content = f.read().splitlines()
    file_name = content[0]
    data = dict()
    for i in range(1, len(content)-1, 3):
        kind = content[i][:-1]
        top1 = float(content[i+1].split(" ")[2])

        line3 = content[i+2].split(" ")
        ta = float(line3[2])
        sem = float(line3[8])
        syn = float(line3[14])
        data[kind] = np.array([top1, ta, sem, syn])

    ll = content[-1].split(" ")
    dic2 = {'seen': ll[4], 'total': ll[5]}
    return data


def main():
    parser = create_parsers()
    args = vars(parser.parse_args())

    se = args['se']
    in_folder = args['f'].rstrip('/')
    out_folder = args['o'].rstrip('/')
    create_output_folder(out_folder)
    csv = args['csv']
    o_csv = args['ocsv']

    # Get draws
    draws = get_sub_dir(in_folder)

    if se == 1:
        draws = ['{}/SE-2012'.format(f) for f in draws]
        # Get configs for each draw, no test to check if configs are equal!
        configs = get_sub_dir(draws[0], flag=0)

        flag = 0
        mean = dict()
        cases = len(draws)
        for config in configs:
            flag = 0
            for draw in draws:
                log = '{0}/{1}/log.csv'.format(draw, config)
                if flag == 0:
                    mean[config] = read_se_log(log)
                    flag = 1
                else:
                    t_data = read_se_log(log)
                    for key in t_data:
                        mean[config][key] += t_data[key]

            for key in mean[config]:
                mean[config][key] /= cases

        save_se_logs(mean, '{}/SE-2012'.format(out_folder))
        fake_csv(csv, o_csv)
    else:
        configs = ['{0}'.format(f.rstrip('.log')) for f in os.listdir(draws[0]) if f.endswith(".log")]
        configs = sorted([f.split('_')[-1] for f in configs])

        mean = dict()
        cases = len(draws)
        for config in configs:
            flag = 0
            for draw in draws:
                print draw
                log = [f for f in os.listdir(draw) if f.endswith('_{}.log'.format(config))][0]
                log = '{}/{}'.format(draw, log)
                if flag == 0:
                    mean[config] = read_log(log)
                    flag = 1
                else:
                    t_data = read_log(log)
                    for key in t_data:
                        mean[config][key] += t_data[key]

            for key in mean[config]:
                mean[config][key] /= cases

        save_sa_logs(mean, out_folder)
        fake_csv(csv, o_csv )
main()