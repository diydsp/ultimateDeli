#!/usr/bin/env bash
# first arg is directory where everything for a specific date is found

dataDir=$1/data

url="https://finviz.com/groups.ashx?g=industry&v=210&o=name"
curl $url -o $dataDir/industry.txt
grep "var rows" $dataDir/industry.txt > $dataDir/rows_industry.txt
