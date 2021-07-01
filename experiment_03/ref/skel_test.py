#!/usr/bin/env python

from subprocess import call
import sys

def hand_train( level, ticker ):
    prg_train     = './train.py'
    str_level         = '--level'
    str_ticker        = '--ticker'
    #train.py    --level m1_100 --ticker STRL
    cmd = [ prg_train, str_level, level, str_ticker, ticker ]
    print cmd
    if live_mode == 1:
        call( cmd )

def hand_eval( level, ticker ):
  prg_eval =      './evaluate.py'
  str_level         = '--level'
  str_ticker        = '--ticker'
  #evaluate.py --level m1_100 --ticker STRL
  cmd = [ prg_eval, str_level, level, str_ticker, ticker ]
  print cmd
  if live_mode == 1:
    call( cmd )

def topN( level, top_percent, mode ):
  prg_eval =      './topN.py'
  str_level         = '--level'
  str_percent       = '--percent'
  str_mode          = '--mode'
  #topN.py --level m1_100 --percent 33 --mode pred
  cmd = [ prg_eval, str_level, level, str_percent, str( top_percent), str_mode, mode ]
  print cmd
  if live_mode == 1:
    call( cmd )
    
def group_eval( in_list, out_level ):
  prg_eval =      './group_eval.py'
  str_in_list       = '--in_list'
  str_out_level     = '--out_level'
  #group_eval.py --in_list   m1_100/top_percent_33_mode_pred.txt \
  cmd = [ prg_eval, str_in_list, in_list, str_out_level, out_level ]
  print cmd
  if live_mode == 1:
    call( cmd )


# start
live_mode = 1

# configure
level_01 = 'm1_100'
level_02 = 'm1_200'

# Hand-enter tickers for Training and Evaluation
ticker   = 'STRL'
hand_train( level_01, ticker )
#sys.exit()
hand_eval( level_01, ticker )

ticker   = 'INSY'
print
hand_train( level_01, ticker )
print
hand_eval( level_01, ticker )

ticker_list = [ 'FBRC', 'FXCM', 'GS'  , 'GCAP',
                'LUK',  'LTS' , 'INTL', 'COWN' ]
for ticker in ticker_list:
    print
    hand_train( level_01, ticker )
    print
    hand_eval( level_01, ticker )


# Screen and Evaluate Best, phase 1
print
topN( level_01, 33, 'pred' )

print
group_eval( level_01 + '/top_percent_33_mode_pred.txt', level_02 )

#topN.py --level m1_100 --percent 33 --mode pred
#group_eval.py --in_list   m1_100/top_percent_33_mode_pred.txt \
#                     --out_level m1_200

# Trade
#python daily/at_PreMarketOpen.py --level m1_300
#python daily/at_MarketOpen.py --level m1_300
#python daily/Strategy.py --level m1_300
#python daily/at_MarketClose.py --level m1_300




