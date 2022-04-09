#!/usr/bin/env python3

import sys
import argparse

def tickers_extract( lines ):
    unique_list = []
    for line in lines:
        spl = line.split( ',' )
        spl = [ ph.replace( '"', '' ) for ph in spl ] # get rid of double quotes
        ticker = spl[ 0 ]
        if ticker not in unique_list:
            unique_list.append( ticker )
    print( unique_list )
        
        
def balance_calc( lines, ticker ):    
    balance = 0
    for line in lines:
        #print( line )
        spl = line.split( ',' )
        spl= [ph.replace('"', '') for ph in spl]
        #print( spl )

        if ticker is not None:
            if spl[ 0 ] != ticker:
                continue

        #print( '-' * 20 )
        #print( spl )                    
               
        if spl[1] == "Filled":

            #print( spl[3])
            transaction = spl[3].split( ' ' )
            #print( transaction )
 
            #print( spl[2] )
            
            print( f'{spl[ 6 ] }, ', end="") # time
            print( f'{transaction[ 0 ]}, ', end="" )   # buy/sell
            print( f'{spl[ 2 ]} ')
            desc = spl[2].split( ' ' )
            #print( desc )
            
            price = float( desc[ 2 ] )
            qty   = int( desc[ 0 ] )
            cost = price * qty
            #print( cost )
            
            if transaction[ 0 ] == 'Buy':
                balance -= cost
            if transaction[ 0 ] == 'Sell':
                balance += cost
                
            print( balance )
            print( )
                                
            
def read_all( filename ):
    with open( filename ) as file:
        lines = file.readlines()
        lines.reverse()
    return lines            


# Arguments
parser = argparse.ArgumentParser()
parser.add_argument( '-et', '--extract-tickers', action="store_true", default=False )
parser.add_argument( dest='filename', type=str, help='input .csv filename' )        
parser.add_argument( dest='tickers', type=str, nargs='?', help='list of ticker names' )
args = parser.parse_args()

# Main program
lines = read_all( args.filename )
if args.extract_tickers:
    print( 'extracting tickers' )
    tickers_extract( lines )
balance_calc( lines, args.tickers )

        

    