#!/usr/bin/env bash
# first arg is directory where everything for a specific date is found

dataDir=$1/data

curl "https://finviz.com/groups.ashx" -o $dataDir/groups.txt
grep "var rows" $dataDir/groups.txt > $dataDir/rows_groups.txt
