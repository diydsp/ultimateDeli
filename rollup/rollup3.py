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
    return unique_list
        
def net_calc( lines, ticker ):    
    net = 0
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
            #print( f'{spl[ 2 ]},  ', end="" )   # x @ y

            desc = spl[2].split( ' ' )
            #print( desc )
            qty   = int( desc[ 0 ] )
            price = float( desc[ 2 ] )
            print( f'{qty}, ', end= "" )
            print( f'${price:.2f}, ', end ="" )
            
            cost = qty * price
            cost = round( cost, 2 )
            print( f'${cost:.2f}, ', end="" )
            
            if transaction[ 0 ] == 'Buy':
                net -= cost
            if transaction[ 0 ] == 'Sell':
                net += cost
            net = round( net, 2 )
            print( f'${net:.2f}, ', end="" )

            print( )
    return net
            
def read_all( filename ):
    with open( filename ) as file:
        lines = file.readlines()[2:]   # skip first two lines
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
tickers_found = tickers_extract( lines )
if args.extract_tickers:
    print( tickers_found )

balance = 0
for ticker in tickers_found:
    print( ticker )
    net = net_calc( lines, ticker )
    balance += net
print( f'Balance, ${balance:.2f}' )

        

    
