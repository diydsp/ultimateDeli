#!/usr/bin/env python3

import json
import ipdb


with open('rows_country.txt') as fin:
    rows = fin.readlines()

st = rows[0]

inside_brackets  = st.split('[')[-1].split(']')[0]
stats = inside_brackets.split( '{' )

#[ print(f'{x}') for x in inside_brackets.split( '{' ) ]
[ print(f'{x}') for x in stats ]

ipdb.set_trace()

for idx in range(1,len(stats)):
    st2 = stats[idx]
    st3 = st2.replace('},', '')
    sp2 = st3.split(',')

    thing = {}

    for pair in sp2:
        if len(pair) > 0:
            ps = pair.split(":")
            tag = ps[0].replace('"', "")
            thing[tag] = ps[1]

    print( thing['ticker'], thing['perfM'], thing['perfW'], thing['perfT'] )
    













