
# Hand-enter tickers for Training and Evaluation
Train( 'm1_100', 'STRL' )
model.h5 Train( level, ticker' )
{
 dir = level + '/' + ticker + '/'
 model_filename = dir + 'model.h5'
 
 return.if( already evaluated( model_filename ) )

 mkdir( dir )
 train_predictions( level, ticker ) # script_gen_xx.py
 model.save( model_filename )
}

Evaluate( 'm1_100', 'STRL' )
eval.h5 Evaluate( level, ticker )
{
 dir = level + '/' + ticker + '/'
 model_filename = dir + 'model.h5'
 model.load( model_filename )
 
 est_predictions()
 est_confidence()
 est_profit( high_tmw / low_tmw )

 eval_filename  = dir + 'eval.h5'
 eval.save( eval_filename )
}

Train( 'm1_100', 'MDT' )
Evaluate( 'm1_100', 'MDT' )
Train( 'm1_100', 'INSY' )
Evaluate( 'm1_100', 'INSY' )
'm1_100'.Report()

Key Files:
evaluation/m1_100/STRL/eval.h5
                 /STRL/model.h5
		      /runlog.txt
                 /MDT/eval.h5
                     /model.h5
		     /runlog.txt		     
                 /INSY/eval.h5
		      /model.h5
		      /runlog.txt
		      
m1_100/STRL/runlog.txt:
test conditions (network size, iterations),
execution log
m1_100/STRL/eval.h5:
prediction score
confidence score
profitability score
m1_100/STRL/model.h5:
Tensorflow model for reloading


Now that several models have been trained and evaluated:

# first screening 
topN( 'm1_100', 1/3, 'pred' ) # > 'm1_100/top_33_percent_pred.h5'

def topN( level, ratio, mode ):

  ticker_list = ticker_list_get( level )
  level_dir
  # read directory listings m1_100/*/eval.h5
  #open( level_dir )
  eval = []
  for ticker in ticker_list:  
    dir = level + '/' + ticker + '/'
    eval_filename = dir + 'eval.h5'
    eval.load( eval_filename )
 
    predictions_get()
    confidence_get()
    profit_get( high_tmw / low_tmw )

    if mode == 'pred':
      score += pred
    if mode == 'predconf':
      score += predconf
    if mode == 'profit':
      score += profit
    eval.append( score )
  
  eval_sorted = sort( eval )

  # save filenames of top ones
  topN_filename  = dir + 'top_' + mode +'.txt'
  topN.save( topN, topN_filename )
  for top_ticker in range( ratio * eval.length() ):
    topN.write( top_ticker )

# second layer eval
group_eval( 'm1_100', 'top_pred', 'm1_200' )

def group_eval( inp_group, inp_mode, level ):
  list_filename = group + '/' + mode + '.txt'
  with open( list_filename ):
    for ticker in group:
      Train( level, ticker )    # > 'm1_200/ticker/model.h5'
      Evaluate( level, ticker ) # > 'm1_200/ticker/eval.h5'
    

# second screening
( 'm1_200' ).topN( 1/3, 'predconf' ) > 'm1_200/top_predconf.txt'
topN( 'm1_200', 1/3, 'predconf' )
topN( level, ratio, mode )


# third layer evaluation
group_eval( 'm1_200', top_predconf', 'm1_300' )

# third screen
topN( 'm1_300', 1/3, 'prof' )  # > 'm1_300/top_prof.txt'
( 'm1_300' ).topN( 1/3, 'prof' ) > 'm1_300_top_prof'



# trading
operating_plans (by_time_period)
-daily       trade
-monthly     scrutinize new candidates 
-quarterly   retune
-halfyear    finance examine
-year        diversify

best_models = 'm1_300_top_prof'
for model in best_models:
  # estimate meta_predictability (confidence) for each feasible opening value
  Daily.At.PreMarketOpen( best_model ) 
PreMarketOpen_Report.txt

for model in best_models:
  Daily.At.MarketOpen( best_model )
MarketOpen_Report.txt

for model in best_models:
  Daily.At.MarketClose( best_model )
MarketClose_Report.txt




Daily.Trading.PreMarketOpen(   # recommend 5pm-6pm

# e.g. +/- 20% of tdy_close
Tickers( database.load( 'm1_300_top_prof' ) )
   .prediction.confidence( hist, tmw_open, 1-.2, 1+.2, 20 )
   .top_N()
   .prediction.candlestick( hist, tmw_open, 1-.2, 1+.2, 20 )
   .top_N()
   .est_profit()
   .top_N()
   .report()
)

Daily.Trading.MarketOpen( # 9:30 am
  .Acquire_opening_data()    # yahoo_API.py 
  .est_confidence( hist, tdy_open )
  .top_N()
  .predictability()  # reduce candidates to N most predictable
  .est.profit( high_tmw / low_tmw )  # estimated profit
  .top_N()
  .report()
)
	
Daily.Trading.Strategy() # 9:35 am
  .price.buy  = tmw_low  + a little 
  .price.sell = tmw_high - a little
  .Now do it IRL in realtime or with e.g. limit orders ()
       .report()
       )

Daily.Trading.MarketClose(  # 430pm 
#roll up results from day
Results().download closings
         .enter trades manually( trades.csv )
         .generate performance plots if time

      actual, pred, ratio, error
open,
close
high
low


