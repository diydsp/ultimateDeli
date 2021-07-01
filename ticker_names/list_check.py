#!/usr/bin/python

# inputs
filename_A = 'list_to_check.txt'
filename_B = 'tickers_unique.txt'

# output
filename_res_out = 'common_tickers.txt'

# read files
set_A = [ i for i in open( filename_A ).readlines() ]
set_B = [ i for i in open( filename_B ).readlines() ]


# perform calcs
intersect = set( set_A ).intersection( set_B )


# results output
res_out = open( filename_res_out, 'w' )
for item in intersect:
    print item
    res_out.write( item )


    
    



