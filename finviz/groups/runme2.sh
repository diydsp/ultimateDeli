#!/usr/bin/env bash
curl "https://finviz.com/groups.ashx?g=industry&v=210&o=name" -o industry.txt
grep "var rows" industry.txt > rows_industry.txt
