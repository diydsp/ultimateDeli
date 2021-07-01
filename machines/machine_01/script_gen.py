#!/usr/bin/python

from subprocess import call

# Execute these two commands to extract a feature and train on it:
#python feature_build_02.py --ticker INSY --ratio_select 10
#python noah_05.py --iter 3 --dims_internal 3

#cmd = [ "python", "./data_ticker_extract.py", ticker_name ]

for ratio_select in range( 0, 16 ):

    #ticker_symbol       = 'PKOH'
    #ticker_symbol       = 'DXPE'
    ticker_symbol       = 'STRL'

    num_iterations      = 200
    internal_dimensions = 20
    
    # get features
    prg_data_extract = './feature_build_02.py'
    ticker           = '--ticker'
    ticker_name      = ticker_symbol
    rat_sel_string   = '--ratio_select'
    rat_sel          = str( ratio_select )
    #cmd = [ "python", prg_data_extract ]
    #cmd = [ 'python' + prg_data_extract + ticker ]
    #cmd = [ 'python', prg_data_extract, ticker, rat_sel_string ]
    cmd = [ prg_data_extract, ticker, ticker_name, rat_sel_string, rat_sel ]
    print
    print cmd
    call( cmd )
    
    # perform learning
    prg_learner          = './noah_05.py'
    iters_str            = '--iter'
    iters_num            = str( num_iterations )
    dims_int_str         = '--dims_internal'
    dims_int_num         = str( internal_dimensions )
    cmd = [ prg_learner, iters_str, iters_num, dims_int_str, dims_int_num ]
    print
    print cmd
    call( cmd )
    
