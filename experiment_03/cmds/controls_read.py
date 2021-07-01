#!/usr/bin/python

# Write the specified controls

import argparse
#import os, sys
import json
import pprint

def read( filename_in ):

    with open( filename_in, 'r') as fff:
        ctrl_struc = json.load( fff )

    return ctrl_struc


if __name__ == '__main__':
   controls_filename = 'controls/controls.json' 
   print "using controls_filename: " + controls_filename

   controls = read( controls_filename )

   print( controls )
