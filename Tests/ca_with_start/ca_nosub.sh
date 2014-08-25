#!/usr/bin/env bash

# first we create the vocab from the corpus
train='../../word2vec/text9'
vocab='vocab1.tmp'
questions='../../word2vec/questions-words.txt'

../../word2vec/word2vec -train $train -save-vocab $vocab -min-count 10

# class-data files that will be used
ca_class='../../ca_classes_data.txt'

# run config
size='300'
config="-size $size -window 11 -sample 0 -hs 1 -negative 0 -min-count 10 -alpha 0.01 -cbow 0 -threads $1"

conf_dir='ca_nosub'
mkdir $conf_dir

t_dir="$conf_dir"

echo $t_dir
for i in 0 1 2 3 4
do
	net="$t_dir/net"
#	First generate the starting network
	../../generate_net.py -v $vocab -c $ca_class -s $size -o $net
#	Then we train
	../../word2vec/word2vec-g -load $net $config -output ${net}_end -train $train -binary 1
	
#	Now we test
	../../word2vec/compute-accuracy ${net}_end 0 < $questions > $t_dir/log_$i
	rm $net ${net}_end
done

rm $vocab
