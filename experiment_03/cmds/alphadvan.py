# basic code to get daily time series from alphaadvantage.com:


# this is the once/per/day OHLCV:
# https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=ATW&apikey=W6QULATJ9IZDXXOF

# this is the once/perminute OHLCV:
# https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=1min&apikey=demo

#import urllib2


class stock_history_request:
    def __init__( self, ticker ):
        self.ticker = ticker

    def make_url( s ):
        url  = ''
        url +='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='
        url += s.ticker
        url += '&apikey=W6QULATJ9IZDXXOF'
        #url ='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=ATW&apikey=W6QULATJ9IZDXXOF'
        return url

    
    

