#!/usr/bin/env python3

'''insert one row into the database'''


import os
from os import listdir
from os.path import isfile, join
import datetime as dt

import sqlite3

import argparse

db_name = "start_times.db"

files_available = []


def parse_args():
    parser = argparse.ArgumentParser(description='Extract data for a single ticker symbol.')
    parser.add_argument('--time_ascii', action="store", dest="time_ascii", help='time to add e.g. 2010_01_06_12_45_00')
    return parser.parse_args()

args = parse_args()

# rebuild database freshly
os.remove( db_name )
# start up database
if not os.path.isfile( db_name ):
    print( "yeah I couldn't find: " + db_name );
    db = sqlite3.connect( db_name )

    
# put single line into database
time_internal = dt.datetime.strptime( args.time_ascii,  "%Y_%m_%d_%H_%M_%S" )
epoch_time = time_internal.timestamp()
entry = [ segs[ 1 ], int( epoch_time ) ]
print( entry )

db.executemany(
    'INSERT INTO Data (date_ascii, date_epoch) VALUES (?, ?)',
    (entry,) )
db.commit()

devmsg = [ segs[ 1 ], epoch_time, len( files_available ) ]
print( devmsg )


