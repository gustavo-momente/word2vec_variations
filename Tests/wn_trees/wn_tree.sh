#!/usr/bin/env bash

# first we create the vocab from the corpus
train='../../word2vec/text9'
vocab='vocab.tmp'

../../word2vec/word2vec -train $train -save-vocab $vocab -min-count 10

for i in 0 1 2 3 4 5 6
do
	../../word_net_tree.py -v $vocab -o wn_tree_$i > log_$i"
	echo "$i"
done

rm $vocab
