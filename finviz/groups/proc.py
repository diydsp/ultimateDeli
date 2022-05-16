#!/usr/bin/env python3

'''
extract useful data from the "groups" data from finviz
'''

import json
import pdb
import argparse

def readData( filename ):    
    with open( filename) as fin:
        rows = fin.readlines()
    return rows


def extractGoodStuff( rows ):
    st = rows[0]
    
    inside_brackets  = st.split('[')[-1].split(']')[0]
    extracted = []
    [ extracted.append( x ) for x in inside_brackets.split( '{' ) ]
    return extracted

parser = argparse.ArgumentParser( description='control learner' )
parser.add_argument( '--date',
                    dest='date',
                    required=True,
                    help='e.g. 2022-05-13  the date to process' )
                    
if __name__ == '__main__':
    args = parser.parse_args()
    date = args.date
    #if date is None:
        
    dataDir = f'{date}/data'    
    procDir = f'{date}/proc'

    dataFile = f'{dataDir}/rows_groups.txt'
    rows = readData( dataFile )
    extracted = extractGoodStuff( rows )

    [ print(x) for x in extracted ]


