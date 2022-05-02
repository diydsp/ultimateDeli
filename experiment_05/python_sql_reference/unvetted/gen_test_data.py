#!/usr/bin/env python3
'''generate empty test data for search algorithm'''

import time
import datetime as dt
import os

test_dir = "test_data"

start_time = dt.datetime( 2010, 7, 4, hour= 3, minute=4, second=6, microsecond=7, tzinfo=None, fold=0)
end_time   = dt.datetime( 2010, 7, 4, hour=10, minute=59, second=12, microsecond=9, tzinfo=None, fold=0)
delta_time = dt.timedelta( seconds = 10 )


current_time = start_time

while current_time <= end_time:
    date_str = current_time.strftime( "%Y_%m_%d_%H_%M_%S" )
    #print( date_str )

    dir = test_dir + "/" + str( date_str )
    #print( dir )
    os.mkdir( dir )
    file = dir + "/" + "rec.wav"
    print( file )
    open( file, 'a' ).close   # create file and close immediately
    
    current_time = current_time + delta_time

    

