#!/usr/bin/python

import argparse
from subprocess import call

# Execute these two commands to extract a feature and train on it:
#./feature_build_02.py --ticker INSY --ratio_select 10
#./noah_05.py --iter 3 --dims_internal 3

parser = argparse.ArgumentParser( description='control trainer' )

parser.add_argument( '--ticker',
                     dest='ticker',
                     help='ticker name, e.g. INSY' )

if __name__ == '__main__':
    args = parser.parse_args()

    print( 'Using ticker', args.ticker ) 

num_iterations      = 10
internal_dimensions = 10
extra_layers        = 5

ratio_list = [ 16,17 ]
#ratio_list = [ 4, 5, 6, 7, 8, 9, 10, 11 ]

ticker = 'HTWR'

live_mode = 0

for ratio_select in ratio_list:

    # calculate features
    prg_data_extract = './feature_build_04.py'
    arg_ticker       = '--ticker'
    ticker_name      = ticker
    rat_sel_string   = '--ratio_select'
    rat_sel          = str( ratio_select )
    cmd = [ prg_data_extract, arg_ticker, ticker, rat_sel_string, rat_sel ]
    print
    print cmd
    if live_mode == 1:
        call( cmd )
    

    # perform learning
    prg_learner          = './noah_07.py'
    iters_str            = '--iter'
    iters_num            = str( num_iterations )
    dims_int_str         = '--dims_internal'
    dims_int_num         = str( internal_dimensions )
    layers_arg_str       = '--extra_layers'
    layers_int_num       = str( extra_layers )
    cmd = [ prg_learner, iters_str, iters_num, dims_int_str, dims_int_num, layers_arg_str, layers_int_num ]
    print
    print cmd
    if live_mode == 1:
        call( cmd )
    

    # store results for judgement
    cmd_cp                = 'cp'
    results_in_filename   = 'tmp/results_out.txt'
    results_out_filename  = 'results/results_'
    results_out_filename += 'ticker_'   + str( ticker         ) + '_'
    results_out_filename += 'ratsel_'   + str( ratio_select   ) + '_'        
    results_out_filename += 'iter_'     + str( iters_num      ) + '_'
    results_out_filename += 'dimsint_'  + str( dims_int_num   ) + '_'
    results_out_filename += 'extlayer_' + str( layers_int_num )
    results_out_filename += '.txt' 
    cmd = [ cmd_cp, results_in_filename, results_out_filename ]
    print
    print cmd
    if live_mode == 1:
        call( cmd )

            
        
