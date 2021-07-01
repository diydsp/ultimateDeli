

# this one saves in onehot class output


import numpy as np

import onehot as oh


input_file = '../../../etf/data/etfs_2016_10_27.csv';
out_dir    = 'data_imported';


convertfunc = lambda x: float(x.strip("%"))/100.

names = ( 'Index',
          'Ticker',
          'Sector',
          'Industry', 
          'MarketCap',
          'PE',
          'ForwardPE',
          'PEG',
          'PS',
          'PB',
          'PCash',
          'PFreeCashFlow',
          'DividendYield',
          'PayoutRatio',
          'EPSttm',
          'EPSgrowththisyear',
          'EPSgrowthnextyear',
          'EPSgrowthpast5years',
          'EPSgrowthnext5years',
          'Salesgrowthpast5years',
          'EPSgrowthquarteroverquarter',
          'Salesgrowthquarteroverquarter',
          'SharesOutstanding',
          'SharesFloat',
          'InsiderOwnership',
          'InsiderTransactions',
          'InstitutionalOwnership',
          'InstitutionalTransactions',
          'FloatShort',
          'ShortRatio',    # 29
          'ReturnonAssets',
          'ReturnonEquity',
          'ReturnonInvestment',
          'CurrentRatio',
          'QuickRatio',
          'LTDebtEquity',
          'GrossMargin',
          'OperatingMargin',
          'ProfitMargin',
          'PerformanceWeek',    #40
          'PerformanceMonth',
          'PerformanceQuarter',
          'PerformanceHalfYear',
          'PerformanceYear',
          'PerformanceYTD',      #45
          'Beta',
          'AverageTrueRange',   # 47
          'VolatilityWeek',
          'VolatilityMonth',
          'ChangefromOpen',
          'AverageVolume',  # 51
          'Price',      # 52
          'Change',
          'Volume')

# note: indices for converters dict are zero-based
my_data = np.genfromtxt( input_file, 
                         #names = names,
                         delimiter=',',
                         skip_header=1,
                         converters={12: convertfunc, # dividend yield
                                     40:convertfunc, 41:convertfunc, 42:convertfunc,  # perf: week, month quarter
                                     43:convertfunc, 44:convertfunc, 45:convertfunc,  # perf: half year, year, YTD
                                     48:convertfunc, 49:convertfunc, # volatility: week, month
                                     50:convertfunc, 53:convertfunc, # change from open, change
                         }
                      )

print( my_data[0] )
print
for idx in range(13,14):
    print( my_data[ idx ] )


print( type( my_data ) )
print( type( my_data[13] ) )
print( my_data.shape )

# congrats, data are now loaded
#################################################



# Make subset of interesting columns
interesting = my_data[ :, [
    #0,   # index
    40,  # perf: week
    #41,42,43,44,45,   # perf: month, quarter, half year, year, YTD
    41, 42,43,44,45,   # perf: month, quarter, half year, year, ShortRatio
    29, 47,52,            # ShortRatio, AverageTrue Range, Volume
]];

print interesting

# remove rows with nans in them
temp = np.ma.masked_invalid( interesting )
nonan = np.ma.compress_rows( np.ma.masked_invalid( interesting ) )
#print 'shape of nonan is'
#print( nonan.shape )


# scale values up by 100 (to make percentage easier to comprehend)
nonan = nonan * 100;





# Make questions
question = nonan[ :, [
    #0,  # perf: week
    1,2,3,4,5,   # perf: month, quarter, half year, year, YTD
    6,7,8,
]];

print question[ 12 ]


# write questions to file
filename_out = out_dir + '/' + 'question.npy';
question_out = open( filename_out, 'w' )
#question_out = open( 'question.npy', 'w' )
np.save( question_out, question )
question_out.close()



#===========================================================

# Make answers
answer = nonan[ :, [
    0,  # perf: week
    #1,2,3,4,5,   # perf: month, quarter, half year, year, YTD
]];

print answer[ 12 ]

# write answers to file
filename_out = out_dir + '/' + 'answer.npy'
answer_out = open( filename_out, 'w' )
#answer_out = open( 'answer.npy', 'w' )
np.save( answer_out, answer )
answer_out.close()


# convert answers to onehot
num_classes = 3
answer_onehot = np.zeros( ( len( nonan), num_classes ) )
for idx, _ in enumerate(nonan):

    val = answer[ idx ]
    class_num = 0
    if val > 0:
        class_num = 1
    if val > 3:
        class_num = 2
#    if val > 1:
#        class_num = 3
#    if val > 2:
#        class_num = 4


    temp = oh.int2onehot( class_num, num_classes )
    for dst_x in range( num_classes ):
        answer_onehot[ idx, dst_x ] = temp[ dst_x ]
        

print( answer_onehot[ 1:200 ] )

# write answer_onehot to file
filename_out = out_dir + '/' + 'answer_onehot.npy'
answer_onehot_out = open( filename_out, 'w' )
#answer_onehot_out = open( 'answer_onehot.npy', 'w' )
np.save( answer_onehot_out, answer_onehot )
answer_onehot_out.close()



#print my_data

#print( my_data[2] )
#print( my_data[3] )
#print( my_data[4] )




