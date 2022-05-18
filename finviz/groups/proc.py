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


def extractRowStuff( rows ):
    st = rows[0]
    
    inside_brackets  = st.split('[')[-1].split(']')[0]
    stats = inside_brackets.split( '{' )
    #extracted = []
    #[ extracted.append( x ) for x in stats ]
    #return extracted
    return stats

def extractGoodStuff( rows ):
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


parser = argparse.ArgumentParser( description='control learner' )
parser.add_argument( '--date',
                    dest='date',
                    required=True,
                    help='e.g. 2022-05-13  the date to process' )
                    
if __name__ == '__main__':
    args = parser.parse_args()
    date = args.date

        
    dataDir = f'{date}/data'    
    procDir = f'{date}/proc'

    dataFile = f'{dataDir}/rows_groups.txt'
    rows = readData( dataFile )
    stats = extractRowStuff( rows )
    #[ print(x) for x in extracted ]
    goodStuff = extractGoodStuff( stats )
    [ print(x) for x in goodStuff ]
    
    


