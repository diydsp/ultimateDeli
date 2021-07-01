#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser( description='control learner' )

parser.add_argument( '--in_list',
                     dest='in_list',
                     help='e.g. m1_100/top_percent_33_mode_pred.txt' )

parser.add_argument( '--out_level',
                     dest='out_level',
                     help='e.g. m1_200' )

if __name__ == '__main__':
    args = parser.parse_args()

    print( 'Using in_list ', args.in_list )
    print( 'Using out_level ', args.out_level ) 

    prg_train = 'train.py'
    cmd = [ prg_train ]
    print cmd

    prg_eval = 'evaluate.py'
    cmd = [ prg_eval ]
    print cmd
    
