
# "functions that help recent_info_read and answer"

from __future__ import print_function

import urllib2
import argparse
import os
import sys
import json
from pprint import pprint


def load_file_into_mem( history_filename ):
   with open( history_filename, 'r' ) as fff:
      hist = json.load( fff )

   #pprint( hist )  # optional pretty print for verification
   return hist

def parse_out_info( hist, date_desired ):

   bbb        = hist[ 'Time Series (Daily)' ][ date_desired ]
   #{u'5. volume': u'449351', u'4. close': u'12.3900', u'2. high': u'12.6300',
   # u'1. open': u'12.1500', u'3. low': u|'12.1000'}

   # extract the fields one-by-one
   t_open   = bbb[ '1. open'   ]
   t_high   = bbb[ '2. high'   ]
   t_low    = bbb[ '3. low'    ]
   t_close  = bbb[ '4. close'  ]
   t_volume = bbb[ '5. volume' ]

   # build a human_readable_string
   out_str  = ''
   out_str += 'OHLCV: '
   out_str += t_open   + ', '
   out_str += t_high   + ', '
   out_str += t_low    + ', '
   out_str += t_close  + ', '
   out_str += t_volume 
   print( out_str )

   # return the OHLCV for the desired date
   return_vec = [ t_open, t_high, t_low, t_close, t_volume ]
   return return_vec
