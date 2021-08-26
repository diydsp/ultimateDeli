import numpy as np


# sim params
seq_len = 100

# synth data
mean = 40.00
stddev = 1

# parameters
cons1 = .1  # number of deviations needed to sell 100%


class Streak:

    def __init__( self, mean, stddev, reserve_val, seq_len, cons1 ):
        self.mean        = mean
        self.stddev      = stddev
        self.reserve_val = reserve_val
        self.seq_len     = seq_len
        self.cons1       = cons1
        self.vals        = np.random.normal( mean, stddev, seq_len )
        self.shares_held = 0
        self.z_score     = 0
        self.num_shares  = 0
        self.verbose     = 1

    #@classmethod
    def printem( self, idx, val, perc_sell, perc_buy ):
        if self.verbose > 0:
            print( f'{idx}, {val:.2f}, {self.z_score:.2f},  [{perc_buy:.2f}, {perc_sell:.2f},]  {self.num_shares:.2f}, {self.shares_held:.2f}, {self.reserve_val:.2f}' )

    #@classmethod
    def sellem( self, num_shares, val ):
        share_value = num_shares * val
        self.shares_held -= num_shares
        self.reserve_val += share_value

    def buyem( self ):
        self.shares_held += self.num_shares
        self.reserve_val -= self.share_value


    #@classmethod
    def run( self ):
        for idx, val in enumerate( self.vals[:-1] ):  # note: must sell on last day
            
            # calculate z-score = ( data point - mean ) / std_dev
            self.z_score = ( val - mean ) / stddev
            perc_sell = 0
            perc_buy  = 0
            if self.z_score > 0:   # sell time
                perc_sell = self.z_score / cons1
                perc_sell = np.minimum( perc_sell, 1.0 )

                self.num_shares = perc_sell * self.shares_held
                self.sellem( self.num_shares, val )    

            else:   # buy time
                perc_buy = -self.z_score / self.cons1
                perc_buy = np.minimum( perc_buy, 1.0 )

                self.share_value = perc_buy * self.reserve_val
                self.num_shares = self.share_value / val
                self.buyem()

            self.printem( idx, val, perc_sell, perc_buy )
        
        # must sell on last day
        val = self.vals[ -1 ]
        idx = len( self.vals )
        perc_sell = 1.0
        self.num_shares = perc_sell * self.shares_held
        self.sellem( self.num_shares, val )    
        
        self.printem( idx, val, perc_sell, perc_buy )


if __name__ == '__main__':

    stddev = 0.1
    while stddev < 2:
        print( f'{stddev:.2f} ')
        endval = []
        num_reps = 100
        for rep in range( num_reps ):
            streak = Streak( mean, stddev, 10000, seq_len, cons1 )
            #if rep != 0:
            streak.verbose = 0
            streak.run()
            #print( f'{streak.reserve_val:.2f} ')
            endval.append( streak.reserve_val )
        mean_end = np.mean( endval )
        std  = np.std( endval )
        growth_per_day = np.exp( np.log( mean_end ) / seq_len )
        print( f'Average, stddev, growth/day: {mean_end:.2f}, {std:.2f}, {growth_per_day:.3f}')

        stddev = stddev +   0.1
