# program to get the names of all the tickers from the huge .csv file
# skim through, make a list of all unique tickers.
#
# not bulletproof, only eliminates sequentially redundant tickers
# might want to convert list to a set to guarantee unique values


# input: .csv file with 'ticker' field (typically first field) as name of ticker
# output: tickers_unique.txt, a list of approx 7000-8000 unique ticker names

import csv


# control parameters
# could go so far as to make thes arguments...
filename_input  = '../data/WIKI_PRICES_212b326a081eacca455e13140d7bb9db.csv'
filename_output = 'tickers_unique.txt'


# main routines begin
ticker_list = []   # main list of unique symbols generated and written to output file

ticker_prev = ''   # temp state variable, previously parsed ticker symbol

# skim through file, building unique ticker names into a list
print( "parsing through file for ticker names" )

with open( filename_input ) as csvfile:
	csvreader = csv.DictReader( csvfile, delimiter=',' )
	for row in csvreader:
		ticker = row[ 'ticker' ]

                if ticker != ticker_prev:
                        ticker_list.append( ticker )
                        print( ticker )
                        ticker_prev = ticker
print( "done parsing out ticker names" )
print( "found ", len( ticker_list ), " ticker names " ) 
# done skimming through file



# now output the file to floppy diskette
print "now writing unique ticker names to floppy diskette"
with open( filename_output, 'w' ) as tickers_out:
        tickers_out.write( '\n'.join( ticker_list ) )
tickers_out.close()
print "done."
# done outputting file to floppy diskette



# //xxx junk begins
#tickers_out = open ( filename_output, 'w' )

#for ticker in ticker_list:
#        print >> tickers_out, ticker
# //xxx junk ends
