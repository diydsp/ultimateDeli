#!/usr/bin/env python3

import json
import pdb


with open('rows_industry.txt') as fin:
    rows = fin.readlines()

st = rows[0]

inside_brackets  = st.split('[')[-1].split(']')[0]
[ print(f'{x}') for x in inside_brackets.split( '{' ) ]
