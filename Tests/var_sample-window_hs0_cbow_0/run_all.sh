#!/usr/bin/env bash

# cp -R ../../Statistics .

change="-size 200 -hs 0 -cbow 0 -negative 8 -alpha 0.025 -threads $1 -min_count 10 -window 2 3 14 -sample 0 0.000005 0.000025"

ca_logs="Logs"
ca_logs_m="${ca_logs}_m"
ca_csv="test_ca.csv"
ca_csv_m="test_ca_m.csv"

se_logs="${ca_logs}_se"
se_logs_m="${se_logs}_m"
se_csv="test_se.csv"
se_csv_m="test_se_m.csv"


for i in 0 1 2
do
# Creating logs from CA
	../../make_logs.py -w2v ../../word2vec/word2vec -train ../../word2vec/text9 -rd ../../run_dics.py ${change} -ca ../../word2vec/compute-accuracy -test ../../word2vec/questions-words.txt -log $ca_csv -folder . -lf $ca_logs/$i
done

# Create mean Log for CA
../../average_logs.py -f $ca_logs -o $ca_logs_m -csv $ca_csv -ocsv $ca_csv_m

# Compress old CA logs and then delete files
cd $ca_logs;tar -zcf ./$ca_logs.tar.gz *;mv ./$ca_logs.tar.gz ..; cd ..; rm -R $ca_logs; mkdir $ca_logs; mv ./$ca_logs.tar.gz $ca_logs

for i in 0 1 2
do
# Create logs from SE-2012
	../../make_logs.py -w2v ../../word2vec/word2vec -train ../../word2vec/text9 -folder $se_logs ${change} -set ../../SE-Test1.py -q ../../SE2012/Testing/Phase1Questions/ -a ../../SE2012/Testing/Phase1Answers/ -SE ../../SE2012 -a2 ../../SE2012/Testing/Phase2Answers/  -folder $se_logs/${i} -log $se_csv
done

# Create mean Log for SE
../../average_logs.py -f $se_logs -o $se_logs_m -csv ${se_logs}/0/${se_csv} -ocsv ${se_logs_m}/$se_csv_m -se

# Compress old SE logs and then delete files
cd $se_logs;tar -zcf ./$se_logs.tar.gz *;mv ./$se_logs.tar.gz ..; cd ..; rm -R $se_logs; mkdir $se_logs; mv ./$se_logs.tar.gz $se_logs

# Create Plots from CA logs
../../log_analyzer.py -f $ca_logs_m -gdl $ca_csv_m  -o Plots -2Ds -cm

# Create Plots from SE-2012 logs
../../log_analyzer.py -se -f $se_logs_m -gdl $se_logs_m/$se_csv_m -o Plots_se -2Ds

# Compres SE plots
cd Plots_se;tar -zcf ./Plots_se.tar.gz *;mv *_Average.png ..;rm *.png;mv ../*_Average.png .; cd ..

# Scores from CA logs
../../sort_results.py -f $ca_logs_m -gdl $ca_csv_m -o scores_ca.csv -cm

# Scores from SE logs
../../sort_results.py -f $se_logs_m -gdl $se_logs_m/$se_csv_m -o scores_se.csv -se

# # creating dictionaries for best case
# gd='../../generate_dics.py -w2v ../../word2vec/word2vec -train ../../word2vec/text9 -folder pca_bin '
# conf=$(../../best_score.sh scores_ca.csv)
# # Bin format
# run="$gd$conf -binary 1 -output bin"
# $run
# # Text format
# run="$gd$conf -binary 0 -output text"
# $run

# # Run pca for success cases
# ../../pca_success.py -caw ../../word2vec/compute-accuracy-w -test ../../word2vec/questions-words.txt -bin pca_bin/bin*.bin -text pca_bin/text*.bin -folder pca/caw -t 0

# # Run pca for all cases
# ../../pca_success.py -nocaw -test ../../word2vec/questions-words.txt -text pca_bin/text*.bin -folder pca/nocaw -t 0

# # Delete dictionaries
# rm -R pca_bin
