#!/usr/bin/env python3

import sys

balance = 0

ticker = sys.argv[ 2 ]

with open( sys.argv[1] ) as file:
    lines = file.readlines()
    
    lines.reverse()
    
    for line in lines:
        #print( line )
        spl = line.split( ',' )
        spl= [ph.replace('"', '') for ph in spl]
        #print( spl )

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
                                
            
            
        
        

    