#!/usr/bin/env bash

# first we create the vocab from the corpus
train='../../word2vec/text9'
vocab='vocab2.tmp'

../../word2vec/word2vec -train $train -save-vocab $vocab -min-count 10

# class-data files that will be used
ca_class='../../ca_classes_data.txt'
no_class='../../no_classes.txt'


# run config
size='300'
config="-size $size -window 11 -sample 0.00002 -hs 1 -negative 0 -min-count 10 -alpha 0.01 -cbow 0 -threads $1"

conf_dir='ca_sub'
mkdir $conf_dir

# first we run with random start
t_dir="$conf_dir/random_start"
mkdir $t_dir

echo $t_dir
for i in 0 1 2
do
	net="$t_dir/net"
	../../generate_net.py -v $vocab -c $no_class -s $size -o $net
	../../word2vec/word2vec-g -load $net $config -output ${net}_end -train $train
	../../rep_dist.py -sn $net -en ${net}_end -c $ca_class  > $t_dir/log${i}
	rm $net ${net}_end
done

# now with start net from generate_net.py using a non-empty class file
t_dir="$conf_dir/ca_classes"
mkdir $t_dir

echo $t_dir
for i in 0 1 2 
do
	net="$t_dir/net"
	../../generate_net.py -v $vocab -c $ca_class -s $size -o $net
	../../word2vec/word2vec-g -load $net $config -output ${net}_end -train $train
	../../rep_dist.py -sn $net -en ${net}_end -c $ca_class  > $t_dir/log${i}
	rm $net ${net}_end
done

rm $vocab
