#!/usr/bin/env bash

# Gets the best configuration from a score.csv file, for usage examples check ./Tests/var_*/run_all.sh

title=$(sed '1q;d' $1)
line=$(sed '2q;d' $1)

# cmd_in = ""
OIFS=$IFS
IFS=','

atitle=( $title )
aline=( $line )

for i in 3 4 5 6 7 8 9 10
do
	cmd="$cmd -${atitle[$i]} ${aline[$i]}"
done

echo "$cmd"

IFS=$OIFS