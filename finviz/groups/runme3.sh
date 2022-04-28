#!/usr/bin/env bash
curl "https://finviz.com/groups.ashx?g=country&v=210&o=name" -o country.txt
grep "var rows" country.txt > rows_country.txt
