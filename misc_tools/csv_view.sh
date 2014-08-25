#!/usr/bin/env bash
# Simple tool to print a csv file in a more convenient way. Usage: ./csv_view.sh file_name csv_separator
	cat "$1" | column -s$2 -t | less -#2 -N -S