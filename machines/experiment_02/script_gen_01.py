#!/usr/bin/python

from subprocess import call

# Execute these two commands to extract a feature and train on it:
#python feature_build_02.py --ticker INSY --ratio_select 10
#python noah_05.py --iter 3 --dims_internal 3

num_iterations      = 10
internal_dimensions = 10
extra_layers        = 5

ratio_list = [ 16,17 ]
#ratio_list = [ 4, 5, 6, 7, 8, 9, 10, 11 ]

ticker_list = [ 'FBRC', 'FXCM', 'GS'  , 'GCAP', 'LUK',  'LTS' , 'INTL', 'COWN',
                'KCG' , 'SCHW', 'GSBD', 'CME' , 'MKTX', 'IBKR', 'MS'  , 'BGCP',
                'LPLA', 'ETFC', 'AMTD' ]
                
#ticker_list = [ 'PKOH', 'DXPE', 'STRL' ]
#ticker_list = [ 'PKOH' ]

live_mode = 1

for ratio_select in ratio_list:

    for ticker_symbol in ticker_list:

    
        # calculate features
        prg_data_extract = './feature_build_03.py'
        ticker           = '--ticker'
        ticker_name      = ticker_symbol
        rat_sel_string   = '--ratio_select'
        rat_sel          = str( ratio_select )
        cmd = [ prg_data_extract, ticker, ticker_name, rat_sel_string, rat_sel ]
        print
        print cmd
        if live_mode == 1:
            call( cmd )
    

        # perform learning
        prg_learner          = './noah_06.py'
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
        results_out_filename  = 'results/results_'
        results_out_filename += 'ticker_'   + str( ticker_symbol  ) + '_'
        results_out_filename += 'ratsel_'   + str( ratio_select   ) + '_'        
        results_out_filename += 'iter_'     + str( iters_num      ) + '_'
        results_out_filename += 'dimsint_'  + str( dims_int_num   ) + '_'
        results_out_filename += 'extlayer_' + str( layers_int_num )
        results_out_filename += '.txt' 
        
        #results_out_filename = 'results_'    + str( ticker_symbol  ) + '_'        + 'ratsel_'   + str( ratio_select   ) + '_'        + 'iter_'     + str( iters_num      ) + '_'        + 'dimsint_'  + str( dims_int_num   ) + '_'        + 'extlayer_' + str( layers_int_num )         + '.txt'
        results_in_filename = 'tmp/results_out.txt'
        cmd_cp             = 'cp'
        cmd = [ cmd_cp, results_in_filename, results_out_filename ]
        print
        print cmd
        if live_mode == 1:
            call( cmd )

            
        
