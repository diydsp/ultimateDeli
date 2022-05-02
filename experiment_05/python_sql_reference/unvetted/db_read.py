#!/usr/bin/env python3

import sqlite3
import datetime as dt

db_name = "start_times.db"

def get_row( epoch_time ):
    db = sqlite3.connect( db_name )
    return db.execute( 'SELECT date_ascii FROM Data WHERE date_epoch = ? ORDER BY id ASC', (epoch_time,))

def get_range( low, high ):
    db = sqlite3.connect( db_name )
    return db.execute( 'SELECT date_ascii,date_epoch FROM Data WHERE date_epoch BETWEEN ? AND ? ORDER BY id ASC', (low,high))
    

def test_get_range():
    # seek ranges
    start_time = dt.datetime( 2010, 7, 4, hour= 3, minute=4, second=6, microsecond=7, tzinfo=None, fold=0)
    end_time   = dt.datetime( 2010, 7, 4, hour=10, minute=59, second=12, microsecond=9, tzinfo=None, fold=0)

    start_time_asc = start_time.strftime( "%Y_%m_%d_%H_%M_%S" )
    end_time_asc   = end_time.strftime( "%Y_%m_%d_%H_%M_%S" )

    start_time_epoch = int( start_time.timestamp() )
    end_time_epoch   = int( end_time.timestamp() )

    print( start_time_epoch, end_time_epoch )

    val = get_range( start_time_epoch, end_time_epoch )

    for row in val:
        print( row )


if __name__ == '__main__':
    test_get_range()



                          
                          
