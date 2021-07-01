


import csv
import numpy as np
import talib

# control parameters
# could go so far as to make these arguments...
ticker_target = 'HTWR'
#ticker_target = 'UHS'
#ticker_target = 'DFS'

# This is for  the informal name
feature_select = 'open_SMA'
#feature_select = 'close_SMA'
#feature_select = 'volume_SMA'
#feature_select = 'SAR'
#feature_select = 'BBands'

# This is the math library function name that gets called
operation_select = 'SMA'
#operation_select = 'SAR'
#operation_select = 'BBands'




# generate filenames
filename_input  = '../cutting_board/ticker_data/ticker_data_' + ticker_target + '.csv'
filename_output = '../cutting_board/features/ticker_data_' + ticker_target + '_' + feature_select + '_' + operation_select + '.csv'

print( filename_input )
print( filename_output )


# choose which columns to load based on feature_select
# column names are:
# ticker,date,open,high,low,close,volume,ex-dividend,split_ratio,adj_open,adj_high,adj_low,adj_close,adj_volume
cols_req = []
if feature_select =='open_SMA':
    cols_req.extend( [ 2 ] )    # 2 should be open price

if feature_select =='close_SMA':
    cols_req.extend( [ 5 ] )    # 5 should be close price

if feature_select =='BBands':
    cols_req.extend( [ 5 ] )    # 5 should be close price
    
if feature_select  == 'volume_SMA':
    cols_req.extend( [ 6 ] )    # 6 should be volume

if feature_select  == 'SAR':
    cols_req.extend( [ 3, 4 ] ) 


# Extract required columns
# this is where extracted fields will go
extracted_field = []
    
# Crawl through input file line-by-line
with open( filename_input ) as csvfile:
    
    # open output file for writing
    with open( filename_output, 'w' ) as data_out:
        out_writer = csv.writer( data_out, delimiter=',' )

        # Header
        
        # initialize data loader
        csvread = csv.reader( csvfile, delimiter=',' )

        # read past input header
        junk = csvread.next()
        
        # write output header
        header = feature_select
        out_writer.writerow( [ header ] )

        # Data
        
        # append to list line by line
        #parsed_count = 0
        for column_tuple in csvread:

            row_out = []
            #print column_tuple
            for col_num in cols_req:
                val = column_tuple[ col_num ]
                #print type(val)
                val2 = float( val )
                row_out.extend( [ val2 ] )
                
            extracted_field.append ( row_out )

            #parsed_count = parsed_count + 1
            #if parsed_count % 1000 == 0:
            #    print( 'parsed = ' + str( parsed_count ) )

        

        # perform feature computation

        # move from python lists to 2d numpy array
        print( type( extracted_field ) )
        print( len( extracted_field ) )
        print( type( extracted_field[ 0 ] ) )
        print( len(  extracted_field[ 0 ] ) )
        print( type( extracted_field[ 0 ][ 0 ] ) )
        print(       extracted_field[ 0 ][ 0 ] )

        indicator_array = np.array( extracted_field, dtype=float )
        print( type( indicator_array ) )
        print(  len( indicator_array ) )


        # translate from indicator name to function call
        if operation_select == 'SMA':     # simple moving average
            input_data = indicator_array[ :, 0 ]
            output = talib.SMA( input_data )
            print( output[ 1:1000 ] )

        if operation_select == 'SAR':     # Parabolic SAR
            high = indicator_array[ :, 0 ]
            low  = indicator_array[ :, 1 ]
            real = talib.SAR(high, low, acceleration=0, maximum=0)
            #print( high )
            #print( low )
            print( real[ 1:1000 ] )

        if operation_select == 'BBands':  # Bollinger Bands
            close = indicator_array[ :, 0 ]
            upperband, middleband, lowerband = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
            print( upperband[ 1:1000 ] )
            

