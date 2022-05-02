#!/usr/bin/env python3

import pdb
import argparse
import pandas as pd

traders=[]

last_price = 40

trader1={'volume':'3000000', 'target':'50' }
trader2={'volume':'-500000', 'target':'25'}


for timeStamp in range(0,7.5*60):
    print('------')
    
    # fill order 
    for trader in traders:
        vol_minutely = trader['volume'] / ( 7.5*60)
        vol2 = vol_minutely

        cost = vol2
        
        

    

