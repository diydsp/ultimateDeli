#!/usr/bin/env python3

"""
parse finviz export, find highest ATR/Price ratio
"""
import pdb
import argparse

import pandas as pd



# Arguments
parser = argparse.ArgumentParser()
parser.add_argument( dest='filename', type=str, help='input .csv filename' )        
args = parser.parse_args()

# making dataframe
df = pd.read_csv( args.filename )

print( df )

mm       = df[[ 'Ticker','Average True Range', 'Price' ]]
mm['Velocity'] = 100 * mm['Average True Range'] / mm['Price'  ]

pd.set_option('display.max_rows',None)
mm = mm.sort_values('Velocity', ascending=False)
print( mm)


#pdb.set_trace()
