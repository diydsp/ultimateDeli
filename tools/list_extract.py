
# extract data for every ticker name in a list of tickers
# runs ticker_data_extract.py on each one
# results in cutting board

from subprocess import call

filename_input = '../experiment_01/tickers.csv'

with open( filename_input ) as tickers_in_file:

    idx = 0
    for line in tickers_in_file:
        idx = idx + 1

        ticker_name = line.strip()
        #print( ticker_name )



        #cmd = [ "python", "./data_ticker_extract.py", ticker_name ]
        #print( cmd )
        #call( cmd )

        # make sure they have a non-trivial length
        # as many tickers' data are NOT in the database
        cmd = [ "ls", "-l", "../cutting_board/ticker_data/ticker_data_" + ticker_name + ".csv" ]
        #print( cmd )
        call( cmd )

        
        
