#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser( description='control learner' )

parser.add_argument( '--level',
                     dest='level',
                     help='training_level, e.g. m1_100' )

parser.add_argument( '--ticker',
                     dest='ticker',
                     help='ticker name, e.g. INSY' )

if __name__ == '__main__':
    args = parser.parse_args()

    print( 'Using level ', args.level )
    print( 'Using ticker', args.ticker ) 
