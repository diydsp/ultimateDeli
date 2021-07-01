python tickers_unique.py    # creates tickers_unique.txt
rm list_to_check.txt
echo STRL >> audition_list.txt
echo MDT  >> audition_list.txt
cat audition_list.txt > list_to_check.txt
python list_check.py        # creates common_tickers.txt

dailies.txt
nonperformers.txt
audition_list.txt



Dailies.Introduction( audition_list.txt )
Dailies.Introduction( audition_list2.txt )
Dailies.Introduction( audition_list3.txt )
Dailies.Operation()

Dailies.Introduction(
   Audition.Assessment( Audition_list )
           .
 )
       .Operation()
       .Preen()


# list of prospective tickers for their qualities
Audition.trainees( list_check.py list_to_check.txt )  # input from trivial CSV 
 .add( existence_in_db() )
 .remove( kill_list.txt )
 .remove( nonperformers.txt )
 .trainees().report()

Audition.def.low()
 .train_predictions.top_N_scores() # script_gen_xx.py
 .est_confidence().top_N_scores() 
 .est_profit( high_tmw / low_tmw ).top_N_scores()
 .recommend() // output list of tickers with report
 .nonperformers_add()  // 

Audition.def.medium()
 .train_predictions.top_N_scores() # script_gen_xx.py
 .est_confidence().top_N_scores()
 .est_profit( high_tmw / low_tmw ).top_N_scores()
 .recommend() // output list of tickers with report
 .deferred()  // remember non-performers


operating_plans (by_time_period)
-daily       trade
-monthly     scrutinize new candidates 
-quarterly   retune
-halfyear    finance examine
-year        diversify

# daily_trading
Dailies.Operation.Previous_Evening(   # 9pm-12am

Tickers( database.load( Dailies.tickers() ) )
   # estimate meta_predictability (confidence) for each feasible opening value
   # e.g. +/- 20% of tdy_close
   .prediction.confidence( hist, tmw_open, 1-.2, 1+.2, 20 )
   .top_N()
   .prediction.candlestick( hist, tmw_open, 1-.2, 1+.2, 20 )
   .top_N()
   .est_profit()
   .top_N()
   .report()
)

Dailies.Operation.Morning( # 9:30 am
  .Acquire_opening_data()    # yahoo_API.py 
  .est_confidence( hist, tdy_open )
  .top_N()
  .predictability()  # reduce candidates to N most predictable
  .est.profit( high_tmw / low_tmw )  # estimated profit
  .top_N()
  .report()
)
	
  .Trading_Strategy() # 9:35 am
  .price.buy  = tmw_low  + a little 
  .price.sell = tmw_high - a little
  .Now do it IRL in realtime or with e.g. limit orders ()
       .report()
       )
	
3. roll up results from day
Operation.Results().download closings
                   .enter trades manually( trades.csv )
                   .generate performance plots if time
