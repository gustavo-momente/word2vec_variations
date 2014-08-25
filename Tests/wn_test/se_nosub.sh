#!/usr/bin/env bash


wn_tree='wn_tree'
r_train='../../word2vec/text9_reshaped'

train='../../word2vec/text9'
vocab='vocab_se_nosub.tmp'

# first we create the vocab from the corpus
../../word2vec/word2vec -train $train -save-vocab $vocab -min-count 10

# run config
size='200'
config="-size $size -window 2 -sample 0 -hs 0 -negative 8 -min-count 10 -alpha 0.025 -cbow 0 -threads $1"


# first  run w2v with the reshaped vocab
t_folder='se_nosub'

mkdir $t_folder

w2v_p1="$t_folder/w2v_p1_tmp"
w2v_p2="$t_folder/w2v_p2_tmp"
w2v_p3="$t_folder/w2v_p3_tmp"


for i in 0 1 2 3
do
	# first we run w2v with the reshaped vocab
	echo ../../word2vec/word2vec -train $r_train $config -binary 0 -output $w2v_p1
	../../word2vec/word2vec -train $r_train $config -binary 0 -output $w2v_p1
	# then we generate the starting configuration for the second iteration
	echo ../../generate_net_from_wn.py -v $vocab -b $w2v_p1 -wn $wn_tree -o $w2v_p2s
	../../generate_net_from_wn.py -v $vocab -b $w2v_p1 -wn $wn_tree -o $w2v_p2
	# now the second iteration
	echo ../../word2vec/word2vec-g -load $w2v_p1 -train $train -read-vocab $vocab -binary 0 $config -output $w2v_p3
	../../word2vec/word2vec-g -load $w2v_p1 -train $train -read-vocab $vocab -binary 0 $config -output $w2v_p3
	# now we test
	echo ../../SE-Test1.py -w $w2v_p3 -q ../../SE2012/Testing/Phase1Questions/ -a ../../SE2012/Testing/Phase1Answers/ -SE ../../SE2012 -a2 ../../SE2012/Testing/Phase2Answers/ -o $t_folder/$i
	../../SE-Test1.py -w $w2v_p3 -q ../../SE2012/Testing/Phase1Questions/ -a ../../SE2012/Testing/Phase1Answers/ -SE ../../SE2012 -a2 ../../SE2012/Testing/Phase2Answers/ -o $t_folder/$i

	rm $w2v_p1 $w2v_p2 $w2v_p3 
done

rm $vocab

