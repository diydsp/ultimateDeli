#!/usr/bin/env python3

import csv
import matplotlib
matplotlib.use( 'Agg' )
import matplotlib.pyplot as plt

from matplotlib.dates import DateFormatter, WeekdayLocate,
    DayLocator, MONDAY
from matplotlib.finance import candlestick_ohlc

import datetime as dt

import numpy as np


def simple_plot( input_file ):

    # Crawl through input file line-by-line
    filename_input = input_file
    rows = []
    with open( filename_input ) as csvfile:

        # initialize data loader
        csvread = csv.reader( csvfile, delimiter=',' )

        # read past input header
        #junk = csvread.next()

        for row in csvread:
            rows.append( row )

    interm = [ x[1:3] for x in rows ]
    rows_np = np.array( interm )
    print( rows_np )
    

    plt.plot( rows_np[:,0], rows_np[:,1], 'x' )
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(15,9)

    #plt.plot( [ 1, 2, 3, 4 ] )
    plt.xlabel( 'mean' )
    plt.ylabel( 'std dev' )
    plt.ylim( [0,0.05] )
    plt.xlim( [0.9, 1.2] )
    plt.savefig( args.plot_output_file )
    #plt.savefig( 'hope.png' )




if __name__ =='__main__':
    parser = argparse.ArgumentParser( description='Plot Gaussian results' )

    parser.add_argument( '-i',
                         dest='input_file',
                         help='input file, e.g. ticker_data.csv' )

    parser.add_argument( '-o',
                     dest='plot_output_file',
                     help='optional output location, e.g. data.csv')
                     
    args = parser.parse_args()



                                                                                                      

