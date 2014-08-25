#!/usr/bin/env bash


# # # hs: 0 cbow: 0
echo "hs: 0 cbow: 0"
# hs0_cbow0 no subsampling 

# creating dictionaries for best case
gd='../../generate_dics.py -w2v ../../word2vec/word2vec -train ../../word2vec/text9 -folder pca_bin'
conf="-size 200 -window 8 -sample 0 -hs 0 -negative 8 -cbow 0 -min_count 10 -alpha 0.025 -threads $1"
case_f='hs0_cbow0_nosub'

# Bin format
run="$gd $conf -binary 1 -output bin"
$run
# Text format
run="$gd $conf -binary 0 -output text"
$run

# Run pca for success cases
../../pca_success.py -caw ../../word2vec/compute-accuracy-w -test ../../word2vec/questions-words.txt -bin pca_bin/bin*.bin -text pca_bin/text*.bin -folder $case_f/caw -t 0

# # Run pca for all cases
../../pca_success.py -nocaw -test ../../word2vec/questions-words.txt -text pca_bin/text*.bin -folder $case_f/nocaw -t 0

# Delete dictionaries
rm -R pca_bin

# hs0_cbow0 with subsampling 

# creating dictionaries for best case
gd='../../generate_dics.py -w2v ../../word2vec/word2vec -train ../../word2vec/text9 -folder pca_bin'
conf="-size 200 -window 11 -sample 0.00002 -hs 0 -negative 8 -cbow 0 -min_count 10 -alpha 0.025 -threads $1"
case_f='hs0_cbow0_sub'

# Bin format
run="$gd $conf -binary 1 -output bin"
$run
# Text format
run="$gd $conf -binary 0 -output text"
$run

# Run pca for success cases
../../pca_success.py -caw ../../word2vec/compute-accuracy-w -test ../../word2vec/questions-words.txt -bin pca_bin/bin*.bin -text pca_bin/text*.bin -folder $case_f/caw -t 0

# # Run pca for all cases
../../pca_success.py -nocaw -test ../../word2vec/questions-words.txt -text pca_bin/text*.bin -folder $case_f/nocaw -t 0

# Delete dictionaries
rm -R pca_bin



# # # hs: 0 cbow: 1
echo "hs: 0 cbow: 1"
# hs0_cbow1 no subsampling 

# creating dictionaries for best case
gd='../../generate_dics.py -w2v ../../word2vec/word2vec -train ../../word2vec/text9 -folder pca_bin'
conf="-size 200 -window 8 -sample 0 -hs 0 -negative 8 -cbow 1 -min_count 10 -alpha 0.025 -threads $1"
case_f='hs0_cbow1_nosub'

# Bin format
run="$gd $conf -binary 1 -output bin"
$run
# Text format
run="$gd $conf -binary 0 -output text"
$run

# Run pca for success cases
../../pca_success.py -caw ../../word2vec/compute-accuracy-w -test ../../word2vec/questions-words.txt -bin pca_bin/bin*.bin -text pca_bin/text*.bin -folder $case_f/caw -t 0

# # Run pca for all cases
../../pca_success.py -nocaw -test ../../word2vec/questions-words.txt -text pca_bin/text*.bin -folder $case_f/nocaw -t 0

# Delete dictionaries
rm -R pca_bin

# hs0_cbow1 with subsampling 

# creating dictionaries for best case
gd='../../generate_dics.py -w2v ../../word2vec/word2vec -train ../../word2vec/text9 -folder pca_bin'
conf="-size 200 -window 5 -sample 0.00002 -hs 0 -negative 8 -cbow 1 -min_count 10 -alpha 0.025 -threads $1"
case_f='hs0_cbow1_sub'

# Bin format
run="$gd $conf -binary 1 -output bin"
$run
# Text format
run="$gd $conf -binary 0 -output text"
$run

# Run pca for success cases
../../pca_success.py -caw ../../word2vec/compute-accuracy-w -test ../../word2vec/questions-words.txt -bin pca_bin/bin*.bin -text pca_bin/text*.bin -folder $case_f/caw -t 0

# # Run pca for all cases
../../pca_success.py -nocaw -test ../../word2vec/questions-words.txt -text pca_bin/text*.bin -folder $case_f/nocaw -t 0

# Delete dictionaries
rm -R pca_bin



# # # hs: 1 cbow: 0
echo "hs: 1 cbow: 0"
# hs1_cbow0 no subsampling 

# creating dictionaries for best case
gd='../../generate_dics.py -w2v ../../word2vec/word2vec -train ../../word2vec/text9 -folder pca_bin'
conf="-size 300 -window 11 -sample 0 -hs 1 -negative 0 -cbow 0 -min_count 10 -alpha 0.01 -threads $1"
case_f='hs1_cbow0_nosub'

# Bin format
run="$gd $conf -binary 1 -output bin"
$run
# Text format
run="$gd $conf -binary 0 -output text"
$run

# Run pca for success cases
../../pca_success.py -caw ../../word2vec/compute-accuracy-w -test ../../word2vec/questions-words.txt -bin pca_bin/bin*.bin -text pca_bin/text*.bin -folder $case_f/caw -t 0

# # Run pca for all cases
../../pca_success.py -nocaw -test ../../word2vec/questions-words.txt -text pca_bin/text*.bin -folder $case_f/nocaw -t 0

# Delete dictionaries
rm -R pca_bin

# hs1_cbow0 with subsampling 

# creating dictionaries for best case
gd='../../generate_dics.py -w2v ../../word2vec/word2vec -train ../../word2vec/text9 -folder pca_bin'
conf="-size 300 -window 11 -sample 0.00002 -hs 1 -negative 0 -cbow 0 -min_count 10 -alpha 0.01 -threads $1"
case_f='hs1_cbow0_sub'

# Bin format
run="$gd $conf -binary 1 -output bin"
$run
# Text format
run="$gd $conf -binary 0 -output text"
$run

# Run pca for success cases
../../pca_success.py -caw ../../word2vec/compute-accuracy-w -test ../../word2vec/questions-words.txt -bin pca_bin/bin*.bin -text pca_bin/text*.bin -folder $case_f/caw -t 0

# # Run pca for all cases
../../pca_success.py -nocaw -test ../../word2vec/questions-words.txt -text pca_bin/text*.bin -folder $case_f/nocaw -t 0

# Delete dictionaries
rm -R pca_bin



# # # hs: 1 cbow: 1
echo "hs: 1 cbow: 1"
# hs1_cbow1 no subsampling 

# creating dictionaries for best case
gd='../../generate_dics.py -w2v ../../word2vec/word2vec -train ../../word2vec/text9 -folder pca_bin'
conf="-size 300 -window 11 -sample 0 -hs 1 -negative 0 -cbow 1 -min_count 10 -alpha 0.01 -threads $1"
case_f='hs1_cbow1_nosub'

# Bin format
run="$gd $conf -binary 1 -output bin"
$run
# Text format
run="$gd $conf -binary 0 -output text"
$run

# Run pca for success cases
../../pca_success.py -caw ../../word2vec/compute-accuracy-w -test ../../word2vec/questions-words.txt -bin pca_bin/bin*.bin -text pca_bin/text*.bin -folder $case_f/caw -t 0

# # Run pca for all cases
../../pca_success.py -nocaw -test ../../word2vec/questions-words.txt -text pca_bin/text*.bin -folder $case_f/nocaw -t 0

# Delete dictionaries
rm -R pca_bin

# hs1_cbow1 with subsampling 

# creating dictionaries for best case
gd='../../generate_dics.py -w2v ../../word2vec/word2vec -train ../../word2vec/text9 -folder pca_bin'
conf="-size 300 -window 11 -sample 0.00002 -hs 1 -negative 0 -cbow 1 -min_count 10 -alpha 0.01 -threads $1"
case_f='hs1_cbow1_sub'

# Bin format
run="$gd $conf -binary 1 -output bin"
$run
# Text format
run="$gd $conf -binary 0 -output text"
$run

# Run pca for success cases
../../pca_success.py -caw ../../word2vec/compute-accuracy-w -test ../../word2vec/questions-words.txt -bin pca_bin/bin*.bin -text pca_bin/text*.bin -folder $case_f/caw -t 0

# # Run pca for all cases
../../pca_success.py -nocaw -test ../../word2vec/questions-words.txt -text pca_bin/text*.bin -folder $case_f/nocaw -t 0

# Delete dictionaries
rm -R pca_bin
