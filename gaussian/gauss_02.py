#!/usr/bin/env python3

"""

simple simuation 
reads data
estimates mean and standard deviation
uses the deviation
to deicde how much to buy/sell
all simplest assumtions made :)

it appears that if you know the mean, not much else matters!
just buy and sell the max amount you can afford depending on
if you're above or below it!
That's a good start, but future sims will make it much more challenging,
by: 
1. Non-gaussian distributoin, but a random walk instead.
2. continuously estimating mean
3. continuously estimating variance

"""

import numpy as np


# sim params
seq_len = 100

# synth data
mean = 352
stddev = 2

# parameters
#cons1 = .1  # number of deviations needed to sell 100%

"""
Run through N days of a gaussian walk.
Given the variance, buy when it's low and sell when it's high
"""

class Streak:

    def __init__( self, mean, stddev, reserve_funds, seq_len, cons1, verbose ):
        self.mean        = mean
        self.stddev      = stddev
        self.reserve_funds = reserve_funds
        self.seq_len     = seq_len
        self.cons1       = cons1
        #self.prices        = np.random.normal( mean, stddev, seq_len )
        self.shares_held = 0
        self.z_score     = 0
        self.num_shares  = 0
        self.verbose     = verbose

    #@classmethod
    def printem( self, day, price, perc_sell, perc_buy ):
        if day == 0:
            print( "day, price, z_score, perc_buy, perc_sell, num_shares, shares_held, reserve_funds" )
        print( f'{day: 3d}, {price:.2f}, {self.z_score: .2f},  [{perc_buy:.2f}, {perc_sell:.2f},]  {self.num_shares:.2f}, {self.shares_held:.2f}, {self.reserve_funds:.2f}' )

    #@classmethod
    def sellem( self, num_shares, price ):
        share_price = num_shares * price
        self.shares_held -= num_shares
        self.reserve_funds += share_price

    def buyem( self ):
        self.shares_held += self.num_shares
        self.reserve_funds -= self.share_price


    #@classmethod
    def run( self ):
        for dayNum, price in enumerate( self.prices[:-1] ):  # note: must sell on last day
            
            # calculate z-score = ( data point - mean ) / std_dev
            self.z_score = ( price - mean ) / stddev
            perc_sell = 0
            perc_buy  = 0
            if self.z_score > 0:   # sell time
                perc_sell = self.z_score / self.cons1
                perc_sell = np.minimum( perc_sell, 1.0 )

                self.num_shares = perc_sell * self.shares_held
                self.sellem( self.num_shares, price )    

            else:   # buy time
                perc_buy = -self.z_score / self.cons1
                perc_buy = np.minimum( perc_buy, 1.0 )

                self.share_price = perc_buy * self.reserve_funds
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


def test_this_cons1( cons1, stddev, prices ):
    for rep in range( num_reps ):
        streak = Streak( mean, stddev, 10000, seq_len, cons1, 0 )  # last is verbose 0/1
        #streak.prices = np.random.normal( mean, stddev, seq_len )
        streak.prices = prices
        #if rep != 0:
        streak.run()
        #print( f'{streak.reserve_funds:.2f} ')
        endprice.append( streak.reserve_funds )
        mean_end = np.mean( endprice )
        std  = np.std( endprice )
        growth_per_day = np.exp( np.log( mean_end ) / seq_len )
    print( f'Const1: {cons1}, Average, stddev, growth/day: {mean_end:.2f}, {std:.2f}, {growth_per_day:.3f}')
            

def test_this_stddev( stddev ):
    for cons1 in np.arange( .1, 10, 2):
        test_this_cons1( cons1, stddev )

def prices_load( filename ):
    price_list=[]
    with open( filename ) as prices_in:
        for row in prices_in:
            srow = ( row.split( ',' ) )
            #print( srow )
            price_list.append( float( srow[ 1 ] ) )
    prices_in.close()
    return price_list

if __name__ == '__main__':

    prices = prices_load( "sample/DIA_1hour_sample.txt" )
    print( prices )
    
    # try for different standard deviations
    for stddev in np.arange( 0.1, .3, 0.1 ):
        print( f'{stddev:.2f} ')
        endprice = []
        num_reps = 100

        for cons1 in np.arange( .1, 10, 2):
            test_this_cons1( cons1, stddev, prices )
        
        #test_this_stddev( stddev )
        

