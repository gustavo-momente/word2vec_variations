#!/usr/bin/python

__author__ = 'vilelag'

import os
import argparse
import subprocess
from multiprocessing import Pool
import itertools
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import matrix_rank
import shutil
from matplotlib import cm
from matplotlib import patheffects
from numpy.ma import masked_array


def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='PCA analysis and Rank analysis of all cases or only '
                                                 'the successful cases.\n For examples check ./Tests/var_*/run_all.sh')
    parser.add_argument('-nocaw', metavar='[<int>]', nargs='?', default=0, type=int, const=1,
                        help='If present all the cases in the <test_file> will be used in the PCA analysis')
    parser.add_argument('-caw', metavar='<compute-accuracy-w_exec>', default='./word2vec/compute-accuracy-w',
                        help='Path to the compute-accuracy-w executable')
    parser.add_argument('-test', metavar='<test_file>', default='./word2vec/questions-words.txt',
                        help='Use text data from <test_file> to test the model')
    parser .add_argument('-bin', metavar='<file.bin>',
                         help='Word representation dictionary in binary mode', required=False)
    parser .add_argument('-text', metavar='<file.bin>', required=True,
                         help='Word representation dictionary in "text" mode')
    parser .add_argument('-folder', metavar='<folder>', default='./pcaImages',
                         help='Folder where all the generated images will be saved')
    parser.add_argument('-threads', metavar='<int>', nargs=1, default=[8], type=int,
                        help='Use <int> threads (default 8)')
    parser.add_argument('-t', metavar='<int>', nargs=1, default=[30000], type=int,
                        help='Threshold is used to reduce vocabulary of the model for fast approximate evaluation '
                             '(0 = off, otherwise typical value is 30000, default=30000)')
    parser.add_argument('-pdf', metavar='<int>', default=1, type=int,
                        help='Decide if the generated tex will be transformed in a pdf (1 = On, else Off, Default: On)')
    return parser


def create_output_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def run_ca(ca, file, threshold, test):
    out = subprocess.check_output([ca, file, threshold], stdin=open(test, 'r'))
    return out


def analyse_log(log):
    classes = dict()
    results = dict()
    current_class = ''
    case = 1
    for line in log.splitlines()[:-1]:
        spt = line.split("\\;")
        # if len(line.split(":")) == 2 and line.split(":")[1] == '':
        if len(spt) == 1 and line[-1] == ':':
            current_class = line[:-1]
        elif len(spt) == 4:
            try:
                classes[current_class].append(spt)
            except KeyError:
                classes[current_class] = [spt]
        else:
            if case == 1:
                results[current_class] = [float(line.split(" ")[2])]
                case = 0
            else:
                tmp = line.split(" ")
                ta = float(tmp[2])
                sem = float(tmp[8])
                syn = float(tmp[14])
                results[current_class].extend([ta, sem, syn])
                case = 1
    return classes, results


def get_raw_classes(test):
    with open(test) as f:
        content = f.read().splitlines()
    classes = dict()
    current_class = ''
    for line in content:
        spt = line.split(' ')
        if len(spt) == 2 and spt[0] == ':':
            current_class = spt[-1]
        elif len(spt) == 4:
            spt = [x.upper() for x in spt]
            try:
                classes[current_class].append(spt)
            except KeyError:
                classes[current_class] = [spt]
    return classes


def read_bin_in_text_mode(path, threshold):
    with open(path) as f:
        content = f.read().splitlines()
    data = dict()
    words, size = content[0].split(' ')
    words = int(words)
    size = int(size)

    if 0 < threshold < words:
        words = threshold
    print words
    for i in range(1, words+1):
        temp = content[i].split(' ')
        data[temp[0].upper()] = np.asarray([float(x) for x in temp[1:-1]])
        # Normalizing
        data[temp[0].upper()] *= 1 / np.linalg.norm(data[temp[0].upper()])

    return data


def get_words_without_repetition(data):
    class_1 = []
    dic_words = dict()
    for i in [0, 2]:
        for datum in data:
            try:
                if dic_words[datum[i]+';'+datum[i+1]]:
                    continue
            except KeyError:
                dic_words[datum[i]+';'+datum[i+1]] = True
                class_1.append([datum[i], datum[i+1]])

    return class_1


def pca_analyse(atuple, confidence_interval=0.9):
    class_name, data = atuple
    data = get_words_without_repetition(data)
    class_representation = []
    for c in data:
        try:
            class_representation.append(wr[c[1]] - wr[c[0]])
        except KeyError:
            pass
    class_representation = np.array(class_representation)
    pca = PCA(n_components=confidence_interval)
    pca.fit(class_representation)

    return class_name, pca.n_components, len(data)


def generate_npc_figure(n_pc):

    y = np.arange(len(n_pc))

    names = tuple((e[0] for e in reversed(n_pc)))
    components = np.array([e[1] for e in reversed(n_pc)])
    comp_div_pair = np.array([float(e[1])/e[2] for e in reversed(n_pc)])
    # print n_pc
    # print comp_div_pair

    fig, (ax0, ax1) = plt.subplots(1, 2, sharey=True, figsize=(18, 16))

    ax0.barh(y, components, align='center',  alpha=0.4)
    plt.yticks(y, names)
    ax0.set_xlabel("Number of components")
    ax0.set_title("Number of components required to get a confidence interval of 90%")
    ax0.grid()

    ax1.barh(y, comp_div_pair, align='center', color='g',  alpha=0.4)
    ax1.set_xlabel("Number of components / number of pairs")
    ax1.set_title("Number of components divided by number of pairs in the class")
    ax1.grid()

    ax1.set_xlim([0, 1])

    ax0.yaxis.set_ticks_position('left')
    ax0.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_ticks_position('left')
    ax1.xaxis.set_ticks_position('bottom')

    plt.savefig(folder+'/ncomponents.png', bbox_inches='tight', transparent=False)
    plt.close()


def pca_analyse2(atuple, link=True):

    class_name, data = atuple
    n_success = len(data)
    data = get_words_without_repetition(data)
    class_1 = []
    class_2 = []
    for c in data:
        try:
            t1 = wr[c[0]]
        except KeyError:
            t1 = None
        try:
            t2 = wr[c[1]]
        except KeyError:
            t2 = None
        if t1 is not None and t2 is not None:
            class_1.append(t1)
            class_2.append(t2)

    class_1 = np.array(class_1)
    class_2 = np.array(class_2)

    pca = PCA(n_components=2)
    pca2 = PCA(n_components=2)

    X_1 = pca.fit(class_1).transform(class_1)
    X_2 = pca2.fit(class_2).transform(class_2)
    print class_name

    plt.figure(figsize=(16, 9))

    plt.scatter(X_1[:, 0], X_1[:, 1], c='r', marker='o')
    plt.scatter(X_2[:, 0], X_2[:, 1], c='b', marker='^')

    # creating links between data1 and data2
    if link:
        for i in range(len(X_1)):
            plt.plot([X_1[i][0], X_2[i][0]], [X_1[i][1], X_2[i][1]], c='gray')

    plt.xlabel("1st PC")
    plt.ylabel("2nd PC")
    plt.title('PCA with 2 PC for {}'.format(class_name))
    plt.figtext(0.1, -0.01, "Number of success cases: {0:<5} Number of combinations: {1}\nFirst explained variance "
                            "ration:      {2}\nSecond explained variance ration: {3}".format(
                n_success, len(data), pca.explained_variance_ratio_, pca2.explained_variance_ratio_))
    plt.savefig(folder+'/'+class_name+'.png', bbox_inches='tight', transparent=False)
    plt.close()


def pca_analyse_all(all_tuples, confidence_interval=0.9):
    data = []
    for cn, datum in all_tuples:
        datum = get_words_without_repetition(datum)
        for el in datum:
            try:
                data.append(wr[el[1]] - wr[el[0]])
            except KeyError:
                pass

    data = np.array(data)

    pca = PCA()
    pca.fit(data)

    ci, n = 0, 0
    for var in pca.explained_variance_ratio_:
        ci += var
        n += 1
        if ci > confidence_interval:
            break


    plt.figure(figsize=(16, 9))
    plt.plot(pca.explained_variance_ratio_)
    #adding confidence_interval vline
    plt.axvline(x=n-1, c='k', linestyle='--')
    plt.xticks(list(plt.xticks()[0]) + [n-1])
    yl = plt.ylim()
    plt.annotate("Number of components\nto {0:.0%} of the distribution".format(confidence_interval),
                 (n-1, (yl[1]-yl[0])/2), ((n-1)/2, (yl[1]-yl[0])/1.6), arrowprops=dict(arrowstyle='->'))
    plt.xlabel("Principal Component")
    plt.ylabel("Explained Variance Ratio")
    plt.title("Explained variance ratio for all the success data")
    plt.savefig(folder+'/evr_all.png', bbox_inches='tight', transparent=False)
    plt.close()


def pca_analyse_all_mean(all_tuples, confidence_interval=0.9):

    data = []
    for cn, datum in all_tuples:
        tmp_data = []
        datum = get_words_without_repetition(datum)
        for el in datum:
            try:
                tmp_data.append(wr[el[1]] - wr[el[0]])
            except KeyError:
                pass
        data.append(np.array(tmp_data).mean(axis=0))
    data = np.array(data)

    pca = PCA()
    pca.fit(data)

    ci, n = 0, 0
    for var in pca.explained_variance_ratio_:
        ci += var
        n += 1
        if ci > confidence_interval:
            break


    plt.figure(figsize=(16, 9))
    plt.plot(pca.explained_variance_ratio_)
    #adding confidence_interval vline
    plt.axvline(x=n-1, c='k', linestyle='--')
    plt.xticks(list(plt.xticks()[0]) + [n-1])
    yl = plt.ylim()
    plt.annotate("Number of components\nto {0:.0%} of the distribution".format(confidence_interval),
                 (n-1, (yl[1]-yl[0])/2), ((n-1)/2, (yl[1]-yl[0])/1.6), arrowprops=dict(arrowstyle='->'))
    plt.xlabel("Principal Component")
    plt.ylabel("Explained Variance Ratio")
    plt.title("Explained variance ratio for the mean of each success in a test class")
    plt.figtext(0.1, -0.01, "Matrix rank: {0}".format(
        matrix_rank(data)))
    plt.savefig(folder+'/evr_mean_all.png', bbox_inches='tight', transparent=False)
    plt.close()


def pca_analyse_combination(data, confidence_interval=0.9):

    data = get_words_without_repetition(data)
    class_1 = []
    for c in data:
        try:
            class_1.append(wr[c[1]] - wr[c[0]])
        except KeyError:
            pass
    class_1 = np.array(class_1)

    pca = PCA(n_components=confidence_interval)

    pca.fit(class_1)

    return pca.n_components


def rank_analyse_combination(data):

    data = get_words_without_repetition(data)
    class_1 = []
    for c in data:
        try:
            class_1.append(wr[c[1]] - wr[c[0]])
        except KeyError:
            pass
    class_1 = np.array(class_1)

    rank = matrix_rank(class_1)
    return rank


def get_element(p_matrix, i, j):
    if i == j:
        return str(p_matrix[i][j])
    sum = p_matrix[i][i] + p_matrix[j][j]
    comb = p_matrix[i][j]
    if comb == sum:
        return str('\\cellcolor{{green!40}} {}'.format(comb))
    elif 0.9*sum < comb < 1.1*sum:
        return str('\\cellcolor{{yellow!40}} {}'.format(comb))
    elif 1.1*sum <= comb:
        return str('\\cellcolor{{orange!40}} {}'.format(comb))
    else: #comb <= 0.9*sum
        return str('\\cellcolor{{red!40}} {}'.format(comb))


def do_line(fd, p_matrix, class_names, i):
    if i == 0:
        t_str = ['&'] + [" \\textbf{{{}}} &".format(name) for name in class_names[:-1]] + \
                [' \\textbf{{{}}} \\\\ \\hline\n'.format(class_names[-1])]
        t_str = ''.join(t_str)
    else:
        t_str = ['\\textbf{{{}}} &'.format(class_names[i-1])] + [" {} &".format(get_element(p_matrix, i-1, j))
                                                                 for j in range(len(p_matrix)-1)] + \
                [' {} \\\\ \\hline\n'.format(get_element(p_matrix, i-1, len(p_matrix)-1))]
        t_str = ''.join(t_str)
    fd.write(t_str)


def generate_latex(class_names, class_names_bak, p_matrix, fname='overlaps'):
    fd = open(folder+"/{}.tex".format(fname), "w")
    fd.write("\\documentclass{report}\n")
    fd.write("\\usepackage{amsmath, amssymb, array, stackengine, subfig}\n")
    fd.write("\\usepackage[table]{xcolor}\n")
    fd.write("\\usepackage[top=2in, bottom=1.5in, left=1cm, right=1cm]{geometry}\n")
    c_width = '{:.3f}\\textwidth'.format(float(0.5)/(len(class_names)))
    fd.write("\\newcolumntype{{C}}{{>{{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{{0pt}}}}m{{{}}}}}\n".format(
        c_width))
    fd.write("\\begin{document}\n")

    # First table
    fd.write('\\begin{tabular}{')
    tstr = ['|'] + ['C|']*(len(class_names)+1)
    tstr = ''.join(tstr)
    fd.write(tstr+'}\n')
    fd.write("\\hline\n")
    fd.write("\\multicolumn{{{}}}{{|c|}}{{\\textbf{{Number of required components to represent each combination}}}}"
             " \\\\ \\hline\n".format(len(class_names)+1))
    for i in range(len(class_names)+1):
        do_line(fd, p_matrix, class_names, i)
    fd.write('\\end{tabular}\n')

    #Creating 'captions'
    fd.write("\\begin{figure}[h]\n")
    # First caption
    fd.write('\\belowbaseline[0pt]{\n\\subfloat{\n\\begin{tabular}{|c|l|}\n')
    fd.write('\\hline\n')
    fd.write('\\multicolumn{2}{|c|}{\\textbf{Label}} \\\\ \\hline\n')
    for i in range(len(class_names)):
        fd.write('\\textbf{{{}}} & {} \\\\ \\hline\n'.format(class_names[i], class_names_bak[i]))
    fd.write('\\end{tabular}\n}}\n')
    # Second caption
    fd.write('\\belowbaseline[0pt]{\n\\subfloat{\n')
    fd.write('\\begin{tabular}{|C|l|}\n\\hline\n')
    fd.write('\\multicolumn{2}{|c|}{\\textbf{Color Meaning}} \\\\ \\hline\n')
    fd.write(' & Class alone  \\\\ \\hline\n')
    fd.write('\\cellcolor{green!40}& $Combination = Sum$ \\\\ \\hline\n')
    fd.write('\\cellcolor{yellow!40}& $0.9 Sum < Combination < 1.1 Sum$ \\\\ \\hline\n')
    fd.write('\\cellcolor{red!40}& $Combination \\leq 0.9 Sum$ \\\\ \\hline\n')
    fd.write('\\cellcolor{orange!40}& $Combination \\geq  1.1 Sum$ \\\\ \\hline\n')
    fd.write('\\end{tabular}\n}}\n')
    fd.write('\\end{figure}\n\n')

    fd.write('\\end{document}\n')
    fd.close()


def generate_pdf(fname='overlaps'):
    subprocess.call(['pdflatex', '{0}/{1}.tex'.format(folder, fname)])
    #remove auxiliary files
    os.remove('{0}.aux'.format(fname))
    os.remove('{0}.log'.format(fname))
    shutil.move('{}.pdf'.format(fname), '{0}/{1}.pdf'.format(folder, fname))


def analyse_combinations(classes, pool, n_pc, pdf, rank=True):
    combinations = [i for i in itertools.combinations(range(len(classes)), 2)]
    class_names = sorted(classes)
    parallel_list2 = [classes[class_names[k[0]]] + classes[class_names[k[1]]] for k in combinations]

    # PCA
    n_pc_comb = pool.map(pca_analyse_combination, parallel_list2)
    p_matrix = [[0]*len(class_names) for i in class_names]
    for i, comb in enumerate(combinations):
        p_matrix[comb[0]][comb[1]] = n_pc_comb[i]
        p_matrix[comb[1]][comb[0]] = n_pc_comb[i]

    class_names_bak = class_names
    class_names = [str(i) for i in range(len(class_names))]
    for i in range(len(class_names)):
        p_matrix[i][i] = n_pc[i][1]

    title = "Number of required components to represent each combination divided by the sum of its elements " \
            "components' number"
    generate_combinations_img(class_names, class_names_bak, p_matrix, title, fname='pca_overlaps_img')
    generate_latex(class_names, class_names_bak, p_matrix, fname='pca_overlaps')

    if pdf == 1:
        generate_pdf(fname='pca_overlaps')

    # Matrix rank
    if rank:
        n_rk_comb = pool.map(rank_analyse_combination, parallel_list2)

        parallel_list3 = [classes[class_names_bak[i]] for i in range(len(classes))]
        n_rk_comb_2 = pool.map(rank_analyse_combination, parallel_list3)


        p_matrix = [[0]*len(class_names) for i in class_names]
        for i, comb in enumerate(combinations):
            p_matrix[comb[0]][comb[1]] = n_rk_comb[i]
            p_matrix[comb[1]][comb[0]] = n_rk_comb[i]

        for i in range(len(class_names)):
            p_matrix[i][i] = n_rk_comb_2[i]

        title = "Matrix rank to represent each combination divided by the sum of its elements rank"
        generate_combinations_img(class_names, class_names_bak, p_matrix, title, fname='rank_overlaps_img')
        generate_latex(class_names, class_names_bak, p_matrix, fname='rank_overlaps')
        if pdf == 1:
            generate_pdf(fname='rank_overlaps')


def generate_combinations_img(class_names, class_names_bak, p_matrix, title, fname='overlaps_img'):
    a_size = len(p_matrix)

    diff = np.zeros([a_size, a_size])

    for i in xrange(a_size):
        for j in xrange(a_size):
            if i == j:
                pass
            else:
                _sum = p_matrix[i][i] + p_matrix[j][j]
                comb = p_matrix[i][j]
                diff[i][j] = float(comb)/float(_sum)

    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)

    diffa = masked_array(diff, diff != 0)
    diffb = masked_array(diff, diff == 0)

    cax = ax.imshow(diffb, cmap=cm.winter, interpolation='None', origin='lower', aspect='auto')
    cba = plt.colorbar(cax, format='%.1f')

    caxb = ax.imshow(diffa, cmap=cm.Reds, interpolation='None', origin='lower', aspect='auto')

    plt.xticks(range(a_size))
    ax.set_xticklabels(class_names_bak)
    plt.xticks(rotation=80)

    plt.yticks(range(a_size))
    ax.set_yticklabels(class_names_bak)

    for i in xrange(a_size):
        for j in xrange(a_size):
            ax.text(j, i, '{0}/{1:.2f}'.format(p_matrix[i][j], diff[i][j]),
                    size='medium', ha='center', va='center',
                    path_effects=[patheffects.withSimplePatchShadow(shadow_rgbFace=(1, 1, 1))])

    plt.title(title)


    # bar = fig.colorbar(cax, format='%.1f')
    plt.rc('text', usetex=True)
    cba.set_label('$\\frac{a_{i,j}}{a_{i,i}+a_{j,j}}$', fontsize=25, rotation=0, labelpad=40)
    plt.savefig(folder+'/'+fname, bbox_inches='tight', transparent=False)
    plt.close()


def main():
    global folder
    global wr
    parser = create_parsers()
    args = vars(parser.parse_args())
    caw = args['caw']
    test = args['test']
    bin = args['bin']
    text_bin = args['text']
    threads = args['threads'][0]
    threshold = str(args['t'][0])
    folder = args['folder']
    pdf = args['pdf']
    nocaw = args['nocaw']

    create_output_folder(folder)
    if nocaw == 0:
        run_output = run_ca(caw, bin, threshold, test)
        classes, results = analyse_log(run_output)
    else:
        classes = get_raw_classes(test)

    wr = read_bin_in_text_mode(text_bin, int(threshold))

    parallel_list = [(k, classes[k]) for k in sorted(classes)]

    pool = Pool(threads)

    n_pc = pool.map(pca_analyse, parallel_list)
    generate_npc_figure(n_pc)

    pool.map(pca_analyse2, parallel_list)

    pca_analyse_all(parallel_list)
    pca_analyse_all_mean(parallel_list)

    analyse_combinations(classes, pool, n_pc, pdf)


folder = ''
wr = dict()
main()