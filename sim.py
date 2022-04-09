#!/usr/bin/env python3

"""
swing trade to target amount
"""

import pdb
import random

# sim params
seq_len = 260  # days


class StockHolding:
    def __init__( self, name, price, qty ):
        self.name = name
        self.price = price
        self.qty = qty

    #@classmethod
    def iterate( self ):
        price = price + random.random()

    #@classmethod
    def print(self):
        print(f'{name}, {price}, {qty}')
        
class Portfolio:
    def __init__( self, stockList ):
        self.stockList = stockList

    #@classmethod
    def print(self):
        for holding in self.stockList:
            holding.print()
        

class Day:

    def __init__( self, portfolio ):
        self.portfolio = portfolio


DayList = []
for dayNumb in range(1,seq_len+1):

    pdb.set_trace()

    # create some stocks
    stock = StockHolding( "abc", 15, 7 )
    stock2 = StockHolding( "xyz", 6, 16 )
    
    portfolio = []
    portfolio.append( stock )
    portfolio.append( stock2 )

    portfolio.print()
    
    DayList[0] = Day( portfolio )
    
    DayList.append( Day( portfolio ) )

    
