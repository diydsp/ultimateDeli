#!/usr/bin/env python3

import argparse
import datetime as dt
import os

parser = argparse.ArgumentParser()
parser.add_argument("-st", "--start-time", action="store", dest="start_time", help="Start time, e.g. 2010_07_04_04_30_06" )
parser.add_argument("-et", "--end-time", action="store", dest="end_time", help="End time, e.g. 2010_07_04_10_56_46" )
parser.add_argument("-de", "--device", action="store", dest="device", help="device name, e.g. muddy-resonance" )
args = parser.parse_args()
    
start_time = dt.datetime.strptime( args.start_time, "%Y_%m_%d_%H_%M_%S" )
end_time   = dt.datetime.strptime( args.end_time ,  "%Y_%m_%d_%H_%M_%S" )
#print( start_time_asc, end_time_asc )

start_time_epoch = str( int( start_time.timestamp() ) )
end_time_epoch   = str( int( end_time.timestamp() ) )
topic_base = "v1/devices/" + args.device + "/rpc/request"
print( start_time_epoch, end_time_epoch )

cmd = "python3  basicPubSubAsync.py " + \
     "--endpoint a18ku8mge40co9-ats.iot.us-east-1.amazonaws.com " + \
     "--rootCA security/AmazonRootCA1.pem " + \
     "--cert xxx " + \
     "--key xxx " + \
     "-id make_request " + \
     "-tb " + topic_base + ' ' + \
     "-ek yes " + \
     "-st " + start_time_epoch + ' ' + \
     "-et " + end_time_epoch + ' '
print( type( cmd ) )

print( cmd )
os.system( cmd )

