#!/usr/bin/env python3

import sys
import pdb

import yaml

with open( sys.argv[1], 'r' ) as file:
    cmdfile = yaml.safe_load( file )

    cmdfile['output']['start_date']  #datetime.date(2021, 8, 12)
    cmdfile['output']['days_back']  # 4




pdb.set_trace()

    
