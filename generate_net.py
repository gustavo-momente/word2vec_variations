#!/usr/bin/python

__author__ = 'vilelag'

import sys
import argparse
import numpy as np


def create_parsers():
    #parser for the main program
    parser = argparse.ArgumentParser(description='Generates a starting network model from vocabulary (vocabulary '
                                                 'exported by word2vec) and class data (in the format of '
                                                 './word2vec/questions-words.txt .\n For a example check'
                                                 ' ./Tests/wn_test/*.sh')
    parser.add_argument('-v', '-vocab', metavar='<file>', required=True,
                        help='Vocabulary file generated by word2vec after analysing a corpus')
    parser.add_argument('-c', '-class', metavar='<file>', required=True,
                        help='File with information about which classes a word belongs')
    parser.add_argument('-s', '-size', metavar='<int>', required=True, type=int,
                        help='Size of the word embedding')
    parser.add_argument('-o', '-output', metavar='<file>', default='generated_net.bin',
                        help='File where the generated net will be saved')
    return parser


def read_vocab(fin):
    with open(fin, 'r') as f:
        content = f.read().splitlines()
    words = dict()
    for line in content:
        tmp = line.split(' ')
        words[tmp[0]] = int(tmp[1])
    try:
        words['</s>'] = sys.maxint
    except KeyError:
        pass

    words = sorted(words, key=words.__getitem__, reverse=True)
    return words


def read_class(fin, vocab):
    with open(fin, 'r') as f:
        content = f.read().splitlines()
    classes = dict()
    word_inclusion = dict()

    for line in content:
        tmp = line.split(' ')
        if tmp[0].lower() not in vocab:
            continue
        word_inclusion[tmp[0].lower()] = tmp[1:]
        for _class in tmp[1:]:
            try:
                classes[_class] += 1
            except KeyError:
                classes[_class] = 1

    classes = sorted(classes, key=classes.__getitem__, reverse=True)
    # classes contains all the classes, the first is the class with most occurrences and the last with the least
    return classes, word_inclusion


def class_representations(classes, size, ref=10):
    n_classes = len(classes)

    if n_classes > size-ref:
        n_classes = size-ref

    class_rep = dict()
    for i in xrange(n_classes):
        class_rep[classes[i]] = np.zeros(size)
        class_rep[classes[i]][i] = 1

    return class_rep


def word_representations(vocab, class_rep, word_inc, size):
    wr = dict()
    for word in vocab:
        # If we have any information about the word class inclusion
        if word in word_inc:
            wr[word] = 0.1*np.random.random(size) - 0.05
            wr[word] /= float(size)
            for rep in word_inc[word]:
                wr[word] += class_rep[rep]

            wr[word] /= np.linalg.norm(wr[word])

        # If we don have any information about its inclusion, we do in the same fashion as word2vec
        else:
            wr[word] = np.random.random(size) - 0.5
            wr[word] /= float(size)

    return wr


def save_net(wr, fout, vocab, size):
    with open(fout, 'w') as f:
        f.write('{} {}\n'.format(len(vocab), size))
        for word in vocab:
            # print type(wr[word])
            # print np.shape(wr[word])
            num = ' '.join(['{0:.6f}'.format(wr[word][i]) for i in xrange(size)])
            f.write('{} {} \n'.format(word, num))


def main():
    parser = create_parsers()
    args = vars(parser.parse_args())
    vocab = args['v']
    _class = args['c']
    _out = args['o']
    size = args['s']

    vocab = read_vocab(vocab)
    classes, wi = read_class(_class, vocab)

    class_rep = class_representations(classes, size, ref=int(size/2))

    used_classes = class_rep.keys()

    # Removing unused classes from wi
    to_remove = []
    for word in wi:
        _remove = [] #stores classes to be removed from wi[word]
        for _class in wi[word]:
            if _class not in used_classes:
                _remove.append(_class)
        # Now we remove those classes
        for _class in _remove:
            wi[word].remove(_class)
        if len(wi[word]) == 0:
            to_remove.append(word)


    for word in to_remove:
        del wi[word]


    words_rep = word_representations(vocab, class_rep, wi, size)
    save_net(words_rep, _out, vocab, size)





main()