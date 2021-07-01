#!/usr/bin/env python

import argparse
from subprocess import call

parser = argparse.ArgumentParser( description='control trainer' )

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

# start

prg_script_gen        = './script_gen_02.py'
arg_ticker            = '--ticker'

live_mode = 1

cmd = [ prg_script_gen, arg_ticker, args.ticker ]
print cmd
if live_mode == 1:
    call( cmd )

