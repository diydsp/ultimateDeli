#!/usr/bin/env python3

'''basic algorithm to respond to requests for files recorded within a certain range'''


import os
from os import listdir
from os.path import isfile, join
import datetime as dt

import sqlite3

import argparse

db_name = "start_times.db"
#import db_store

location = "/data/rec_data"

files_available = []

# r=>root, d=>directories, f=>files
files_in_dir = []
countdown = 0


def parse_args():
    parser = argparse.ArgumentParser(description='Extract data for a single ticker symbol.')
    parser.add_argument( '--build',
                         dest='build',
                         help='level name, e.g. m1_100' )

    parser.add_argument( '--ticker',
                         dest='ticker',
                        help='ticker name, e.g. INSY' )
    #parser.add_argument('ticker', type=str, help='ticker symbol')
    #parser.add_argument( 'level', type=str, help='level, e.g. m1_100' )
    return parser.parse_args()



args = parse_args()

# rebuild database freshly
try:
    os.remove( db_name )
except:
    print( "database not there so wont delete" )
    
# start up database
if not os.path.isfile( db_name ):
    print( "yeah I couldn't find: " + db_name );
    db = sqlite3.connect( db_name )
    db.execute('CREATE TABLE Data (id INTEGER PRIMARY KEY ASC, date_ascii TEXT, date_epoch INT32)')
    db.commit()

    
# put all directory names into database
time_start = dt.datetime.now()
for root, dirs, files in os.walk(location):
    for item in files:
        if '.wav' in item:
            #print( root, dirs, files, item )
            files_in_dir.append(os.path.join(root, item))

            segs = root.split( '/' )
            print( segs )
            time_rec = segs[ 3 ]

            try:            
                time_internal = dt.datetime.strptime( time_rec,  "%Y_%m_%d_%H_%M_%S" )
                epoch_time = time_internal.timestamp()

                entry = [ time_rec, int( epoch_time ) ]
                files_available.append( entry )

                db.executemany(
                    'INSERT INTO Data (date_ascii, date_epoch) VALUES (?, ?)',
                (entry,) )
                #db.commit()
            
                countdown = countdown - 1
                if countdown <= 0:
                    countdown = 100
                    devmsg = [ time_rec, epoch_time, len( files_available ) ]
                    print( devmsg )
            except:
                print( "not valid: ", time_rec )



db.commit()
print('indexing the database')
db.execute('CREATE INDEX date_idx ON Data (date_epoch)')
                
# on WSL:
# takes about 8 milliseconds per file...  720 files per hour = 34560 files in 2 days, means 276 seconds to scan them all
# 
time_end = dt.datetime.now()
time_delta = time_end - time_start
print( "time to scan ", len( files_available ), " files is: ", time_delta )
print( "time per file is: ", time_delta / len( files_available ) )

