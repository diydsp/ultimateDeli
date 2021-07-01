
import numpy as np
import sklearn
from sklearn.utils import shuffle
import sklearn

rows_num = 10

cols_q_num = 4

cols_a_num = 3


# build question
entries_q = cols_q_num * rows_num
q = np.arange( entries_q ).reshape( ( rows_num, cols_q_num ) )

print( q )


# build answer
entries_a = cols_a_num * rows_num
a = np.arange( entries_a ).reshape( ( rows_num, cols_a_num ) )
print( a )




q, a = shuffle( q, a, random_state = 0 )

print ( q )
print ( a )



