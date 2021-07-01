#!/usr/bin/python

# build question vecture from daily ticker data
# in _02, it reads entire file in before creating output
# so that questions spanning several days can be created

import csv
import numpy as np
import talib

import argparse

import onehot as oh

parser = argparse.ArgumentParser( description='control learner' )

parser.add_argument( '--ticker',
                     dest='ticker',
                     help='ticker symbol, e.g. INSY' )

parser.add_argument( '--ratio_select',
                     dest='ratio_select',
                     help='select which ratio to train on, e.g. 1 through 16' )

if __name__ == '__main__':
    args = parser.parse_args()

    print( 'Using ratio_select ', args.ratio_select )
    print( 'Using ticker', args.ticker ) 


# control parameters

ticker_target = args.ticker


# generate filenames
out_dir    = 'data_imported';
filename_input  = '../../cutting_board/ticker_data/ticker_data_' + ticker_target + '.csv'
filename_output = '../../cutting_board/features/ticker_data_' + ticker_target + '_' + '.csv'

print( filename_input )
print( filename_output )


# choose which columns to load based on feature_select
# column names are:
# ticker,date,open,high,low,close,volume,ex-dividend,split_ratio,adj_open,adj_high,adj_low,adj_close,adj_volume
cols_req = []
#cols_req.extend( [ 2, 3, 4, 5, 6 ] )  # open,hight,low,close,volume 
cols_req.extend( [ 2, 3, 4, 5 ] )   # open, high,low,close


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
        header = "daily_stuff"
        #out_writer.writerow( [ header ] )    # TEMPORARILY DISABLED!!!!


        # Data
        # read whole input array(s) in
        ohlc = []
        for column_tuple in csvread:

            row_out = []
            #print column_tuple
            for col_num in cols_req:
                val = column_tuple[ col_num ]
                #print type(val)
                val2 = float( val )
                row_out.extend( [ val2 ] )
                
            ohlc.append ( row_out )


        # create question vectors from input array(s)
        for idx in range( len( ohlc ) - 2 ):

            row_temp = []
            row_temp[ 0:3 ] = ohlc[     idx ]       # ohlc
            row_temp[ 4:7 ] = ohlc[ 1 + idx ]       # ohlc
            row_temp.append( ohlc[ 2 + idx ][ 0 ] ) # o_tmw
            #print( idx, row_temp )
            #print( ohlc[ idx ] )
            extracted_field.append ( row_temp )
            #print( idx, extracted_field )

        # at this point, extracted_field is the python list
        # and indicator_array is the numpy array

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
        print( indicator_array.shape )
        print( indicator_array )
        


        # write questions to file
        filename_out = out_dir + '/' + 'question.npy';
        question_out = open( filename_out, 'w' )
        indic_arr_len = len( indicator_array )
        # note predicting following day, so N-1 data rows
        np.save( question_out, indicator_array[ 0: indic_arr_len - 1 ] )
        question_out.close()


        # create answers
        # convert answers to onehot
        num_classes = 3
        answer_onehot = np.zeros( ( len( indicator_array ) - 1, num_classes ) )

        # first compute all ratios
        ratios = np.zeros( indic_arr_len )
        ratio_select = int( args.ratio_select )
        print( 'Using ratio_select ', ratio_select )
        if ratio_select == None:
            quit()
        for idx in range( indic_arr_len - 2 ):

            open_yest   = indicator_array[ 0 + idx ][ 0 ]
            high_yest   = indicator_array[ 0 + idx ][ 1 ]
            low_yest    = indicator_array[ 0 + idx ][ 2 ]
            close_yest  = indicator_array[ 0 + idx ][ 3 ]

            open_today  = indicator_array[ 1 + idx ][ 0 ]
            high_today  = indicator_array[ 1 + idx ][ 1 ]
            low_today   = indicator_array[ 1 + idx ][ 2 ]
            close_today = indicator_array[ 1 + idx ][ 3 ]
            
            open_tmw    = indicator_array[ 2 + idx ][ 0 ]
            high_tmw    = indicator_array[ 2 + idx ][ 1 ]
            low_tmw     = indicator_array[ 2 + idx ][ 2 ]
            close_tmw   = indicator_array[ 2 + idx ][ 3 ]

            if ratio_select == 16:
                ratio = high_tmw / open_tmw
            if ratio_select == 17:
                ratio = low_tmw / open_tmw
            if ratio_select == 18:
                ratio = close_tmw / open_tmw


            if ratio_select == 0:
                ratio = open_tmw / open_today
            if ratio_select == 1:
                ratio = open_tmw / high_today
            if ratio_select == 2:
                ratio = open_tmw / low_today
            if ratio_select == 3:
                ratio = open_tmw / close_today

            if ratio_select == 4:
                ratio = high_tmw / open_today
            if ratio_select == 5:
                ratio = high_tmw / high_today
            if ratio_select == 6:
                ratio = high_tmw / low_today
            if ratio_select == 7:
                ratio = high_tmw / close_today

            if ratio_select == 8:
                ratio = low_tmw / open_today
            if ratio_select == 9:
                ratio = low_tmw / high_today
            if ratio_select == 10:
                ratio = low_tmw / low_today
            if ratio_select == 11:
                ratio = low_tmw / close_today
                
            if ratio_select == 12:
                ratio = close_tmw / open_today
            if ratio_select == 13:
                ratio = close_tmw / high_today
            if ratio_select == 14:
                ratio = close_tmw / low_today
            if ratio_select == 15:
                ratio = close_tmw / close_today

            #print( ratio )
            ratios[ idx ] = ratio
            
        # auto-generate thresholds
        sorted_ratios = np.sort( ratios )
        #for idx in range( len( sorted_ratios )):
        #    print( sorted_ratios[ idx ] )
        index_upper = int( 0.666 * indic_arr_len )
        index_lower = int( 0.333 * indic_arr_len )
        thresh_upper = sorted_ratios[ index_upper ]
        thresh_lower = sorted_ratios[ index_lower ]
        print( thresh_upper )
        print( thresh_lower )

        # now classify each ratio
        for idx in range( indic_arr_len - 1 ):

            class_num = 1
            if ratios[ idx ] > thresh_upper:
                class_num = 2
            if ratios[ idx ] < thresh_lower:
                class_num = 0

            temp = oh.int2onehot( class_num, num_classes )
            for dst_x in range( num_classes ):
                answer_onehot[ idx, dst_x ] = temp[ dst_x ]
                        
            
        print( answer_onehot[ 1:800 ] )
        print answer_onehot.sum( axis = 0 )
                        
        # write answer_onehot to file
        filename_out = out_dir + '/' + 'answer_onehot.npy'
        answer_onehot_out = open( filename_out, 'w' )
        #answer_onehot_out = open( 'answer_onehot.npy', 'w' )
        np.save( answer_onehot_out, answer_onehot )
        answer_onehot_out.close()




        # different type of answer, non-categorized
        answer = np.zeros( ( len( indicator_array ) - 1 ) )
        for idx in range( indic_arr_len - 1 ):

            open_tmw  = indicator_array[ 1 + idx ][ 0 ]
            answer[ idx ] = open_tmw

        # write answer to file
        filename_out = out_dir + '/' + 'answer.npy'
        answer_out = open( filename_out, 'w' )
        np.save( answer_out, answer )
        answer_out.close()
    
        

