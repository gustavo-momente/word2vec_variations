#!/usr/bin/env bash

i=$1
vocab='vocab.tmp'

../../word_net_tree.py -v $vocab -o wn_tree_$i > log_$i
echo "$i"
