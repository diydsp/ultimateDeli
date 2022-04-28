#!/usr/bin/env bash
curl "https://finviz.com/groups.ashx" -o groups.txt
grep "var rows" groups.txt > rows_groups.txt
