
#!/usr/bin/env python

"""Extract data for a single ticker symbol.

NOTE: row[0] of the input CSV file must be the ticker field.

"""

import argparse
import csv
import os
import sqlite3


#FILENAME_INPUT  = '../data/WIKI_PRICES_212b326a081eacca455e13140d7bb9db.csv'
#DB_NAME = FILENAME_INPUT.replace('.csv', '.db')



def parse_args():
    parser = argparse.ArgumentParser(description='Extract data for a single ticker symbol.')
    parser.add_argument( '--level',
                         dest='level',
                         help='level name, e.g. m1_100' )

    parser.add_argument( '--ticker',
                         dest='ticker',
                         help='ticker name, e.g. INSY' )
    #parser.add_argument('ticker', type=str, help='ticker symbol')
    #parser.add_argument( 'level', type=str, help='level, e.g. m1_100' )
    return parser.parse_args()


def header_row():
     with open(FILENAME_INPUT) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        return next(reader)

def index_database():
    print('indexing the database')
    db.execute('CREATE INDEX ticker_idx ON Data (ticker)')
        
def insert_database( tuple ):
    db.executemany(
        'INSERT INTO Data (ticker, raw) VALUES (?, ?)',
        ((x[0], ','.join(x)) for x in reader))
    db.commit()
    
    
def build_database( DB_NAME ):
    if not os.path.isfile(DB_NAME):
        print( "yeah I couldn't find" + DB_NAME );
        db = sqlite3.connect(DB_NAME)
        db.execute('CREATE TABLE Data (id INTEGER PRIMARY KEY ASC, ticker TEXT, raw BLOB)')
        db.commit()
        
#        with open(FILENAME_INPUT) as csvfile:
#            reader = csv.reader(csvfile, delimiter=',')
#            next(reader)
#            print('loading the database')

#            db.executemany(
#                'INSERT INTO Data (ticker, raw) VALUES (?, ?)',
#                ((x[0], ','.join(x)) for x in reader))
#            db.commit()

#        print('indexing the database')
#        db.execute('CREATE INDEX ticker_idx ON Data (ticker)')


def rows_for_ticker(ticker):
    db = sqlite3.connect(DB_NAME)
    return db.execute(
        'SELECT raw FROM Data WHERE ticker = ? ORDER BY id ASC',
        (ticker,))
    
        
def process(args):

    #level_list/m1_100/tick_list/INSY/class/features/
    filename_output = 'level_list/' + args.level + '/tick_list/' + args.ticker + '/class/features/ticker_data.csv'
    #filename_output = 'level_list/' + args.level + '/tick_list/' + args.ticker + '/class/features/ticker_data_{}.csv'.format( args.ticker )
    #filename_output = '../cutting_board/ticker_data/ticker_data_{}.csv'.format(args.ticker)
    header = header_row()
    print('Writing to ' + filename_output)
    print(header)
    with open(filename_output, 'w') as data_out:
        data_out.write(','.join(header) + '\n')
        for row in rows_for_ticker(args.ticker):
            data_out.write(row[0] + '\n')


#if __name__ == '__main__':
#    args = parse_args()
#    build_database()
#    process(args)
    
