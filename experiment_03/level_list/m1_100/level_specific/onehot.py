# -*- coding: utf-8 -*-
'''onehot encoder
'''

from __future__ import print_function
import numpy as np


def int2onehot( index, len ):
    onehot_out = np.zeros( ( len, 1 ) );
    onehot_out[ index ] = 1;
    return onehot_out

def onehot2int( vec ):
    index = np.argmax( vec )
    return index



#
#    def encode(self, C, maxlen=None):
#        maxlen = maxlen if maxlen else self.maxlen
#        X = np.zeros((maxlen, len(self.chars)))
#        for i, c in enumerate(C):
#            X[i, self.char_indices[c]] = 1
#        return X
#
#    def decode(self, X, calc_argmax=True):
#        if calc_argmax:
#            X = X.argmax(axis=-1)
#        return ''.join(self.indices_char[x] for x in X)
#
#    
#    X[i] = ctable.encode(sentence, maxlen=MAXLEN)
#for i, sentence in enumerate(expected):
#    y[i] = ctable.encode(sentence, maxlen=DIGITS + 1)
#
#
#
#
#
#
#    q = ctable.decode(rowX[0])
#        correct = ctable.decode(rowy[0])
#        guess = ctable.decode(preds[0], calc_argmax=False)

        
