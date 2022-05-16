#!/usr/bin/env python3

'''
Make output directory
Download data into it
Run the report processing on it
'''
import datetime as dt
from subprocess import call
import os

# controls whether we only print cmds or also run them
live_mode = 1


def makeEasyDateString( date ):
    return date.strftime("%Y-%m-%d")


def dir_add( dir_name ):
    print( 'going to add dir: ' + dir_name )    

    if os.path.exists( dir_name ):
        print( 'already found: ' + dir_name )
    else:
        os.mkdir( dir_name, 0o755 )
        
        
# Make output directories
dateToday = dt.datetime.today()
dateStr = makeEasyDateString( dateToday )
dataDir = f'{dateStr}/data'
procDir = f'{dateStr}/proc'
dir_add( dateStr )
dir_add( dataDir )
dir_add( procDir )

# Download data into it
cmd1 = [ './runme.sh', dataDir ]
cmd2 = [ './runme2.sh', dataDir ]
cmd3 = [ './runme3.sh', dataDir ]
print( cmd1 )
print( cmd2 )
print( cmd3 )
if live_mode == 1:
    call( cmd1 )
    call( cmd2 )
    call( cmd3 )
    

# Run the report processing on it


