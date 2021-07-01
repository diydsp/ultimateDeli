#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser( description='control learner' )

parser.add_argument( '--level',
                     dest='level',
                     help='training_level, e.g. m1_100' )

parser.add_argument( '--percent',
                     dest='top_percent',
                     help='e.g. --percent 33 means keep top third' )

parser.add_argument( '--mode',
                     dest='mode_score',
                     help='--mode pred/predconf/prof' )

if __name__ == '__main__':
    args = parser.parse_args()

    print( 'Using level ', args.level )
    print( 'Using percent', args.top_percent )
    print( 'Using mode', args.mode_score )

    
