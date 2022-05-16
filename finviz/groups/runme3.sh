#!/usr/bin/env bash
# first arg is directory where everything for a specific date is found

dataDir=$1/data

url="https://finviz.com/groups.ashx?g=country&v=210&o=name"
curl $url -o $dataDir/country.txt
grep "var rows" $dataDir/country.txt > $dataDir/rows_country.txt
