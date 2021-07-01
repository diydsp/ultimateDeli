To run this:

python feature_calc.py

It tells you input and output filenames:
input:  ../cutting_board/ticker_data/ticker_data_UHS.csv
output: ../cutting_board/features/   ticker_data_UHS_open_SMA.csv

Variables to be set to control it are:
ticker_target = 'HTWR'

# This is for  the informal name
feature_select = 'open_SMA'

# This is the math library function name that gets called
operation_select = 'SMA'





