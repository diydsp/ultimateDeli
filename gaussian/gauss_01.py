#!/usr/bin/env python3


import numpy as np


# sim params
seq_len = 100

# synth data
mean = 40.00
stddev = 1

# parameters
cons1 = .1  # number of deviations needed to sell 100%

"""
Run through N days of a gaussian walk.
Given the variance, buy when it's low and sell when it's high
"""

class Streak:

    def __init__( self, mean, stddev, reserve_price, seq_len, cons1, verbose ):
        self.mean        = mean
        self.stddev      = stddev
        self.reserve_price = reserve_price
        self.seq_len     = seq_len
        self.cons1       = cons1
        self.prices        = np.random.normal( mean, stddev, seq_len )
        self.shares_held = 0
        self.z_score     = 0
        self.num_shares  = 0
        self.verbose     = verbose

    #@classmethod
    def printem( self, day, price, perc_sell, perc_buy ):
        if day == 0:
            print( "day, price, z_score, perc_buy, perc_sell, num_shares, shares_held, reserve_price" )
        print( f'{day}, {price:.2f}, {self.z_score:.2f},  [{perc_buy:.2f}, {perc_sell:.2f},]  {self.num_shares:.2f}, {self.shares_held:.2f}, {self.reserve_price:.2f}' )

    #@classmethod
    def sellem( self, num_shares, price ):
        share_price = num_shares * price
        self.shares_held -= num_shares
        self.reserve_price += share_price

    def buyem( self ):
        self.shares_held += self.num_shares
        self.reserve_price -= self.share_price


    #@classmethod
    def run( self ):
        for dayNum, price in enumerate( self.prices[:-1] ):  # note: must sell on last day
            
            # calculate z-score = ( data point - mean ) / std_dev
            self.z_score = ( price - mean ) / stddev
            perc_sell = 0
            perc_buy  = 0
            if self.z_score > 0:   # sell time
                perc_sell = self.z_score / cons1
                perc_sell = np.minimum( perc_sell, 1.0 )

                self.num_shares = perc_sell * self.shares_held
                self.sellem( self.num_shares, price )    

            else:   # buy time
                perc_buy = -self.z_score / self.cons1
                perc_buy = np.minimum( perc_buy, 1.0 )

                self.share_price = perc_buy * self.reserve_price
                self.num_shares = self.share_price / price
                self.buyem()

            if self.verbose == 1:
                self.printem( dayNum, price, perc_sell, perc_buy )
        
        # must sell on last day
        price = self.prices[ -1 ]
        dayNum = len( self.prices )
        perc_sell = 1.0
        self.num_shares = perc_sell * self.shares_held
        self.sellem( self.num_shares, price )    
        
        if self.verbose == 1:
            self.printem( dayNum, price, perc_sell, perc_buy )


if __name__ == '__main__':

    for stddev in np.arange(0.1,5,0.5):
        print( f'{stddev:.2f} ')
        endprice = []
        num_reps = 100
        for rep in range( num_reps ):
            streak = Streak( mean, stddev, 10000, seq_len, cons1, 0 )  # last is verbose 0/1
            #if rep != 0:
            streak.run()
            #print( f'{streak.reserve_price:.2f} ')
            endprice.append( streak.reserve_price )
        mean_end = np.mean( endprice )
        std  = np.std( endprice )
        growth_per_day = np.exp( np.log( mean_end ) / seq_len )
        print( f'Average, stddev, growth/day: {mean_end:.2f}, {std:.2f}, {growth_per_day:.3f}')

