# extract data for a single ticker symbol
# NOTE: this requires that row[0] is the ticker field
# should your file format change, you will want to point to the new positoin ofthe ticker
# (or better yet auto-extract it )

import csv

# first extract data for this ticker

# control parameters
# could go so far as to make these arguments...
ticker_target = 'UHS'
filename_input  = '../data/WIKI_PRICES_212b326a081eacca455e13140d7bb9db.csv'
filename_output = '../cutting_board/ticker_data/ticker_data_' + ticker_target + '.csv'

# stats
parsed_count = 0
matched_count = 0

# open output file for writing
with open( filename_output, 'w' ) as data_out:
    out_writer = csv.writer( data_out, delimiter=',' )

    print( 'Writing to ' + filename_output )
    
    # skim through input file line-by-line
    with open( filename_input ) as csvfile:

        csvread = csv.reader( csvfile, delimiter=',' )

        # copy header
        header = csvread.next()
        print( header )
        out_writer.writerow( header )

        # copy line by line
        for row in csvread:

            ticker = row[ 0 ]             
            if ticker == ticker_target:
                out_writer.writerow( row )
                matched_count = matched_count + 1

            parsed_count = parsed_count + 1
            if parsed_count % 1000000 == 0:
                print( 'match,parsed = ', matched_count, ',' , parsed_count )

# clean up
data_out.close()

        





# // xxx
# junk
#
#line_first = csvread.next()
#print( line_first )
#print >> data_out, line_first
#
# // xxx
                # print >> data_out, row
