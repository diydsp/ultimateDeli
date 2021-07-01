# -*- coding: utf-8 -*-
'''predict weekly performance of equities from features
this one turns the requested output feature into onehot class
'''

from __future__ import print_function
from keras.models import Sequential
from keras.engine.training import slice_X
from keras.layers import Activation, TimeDistributed, Dense, RepeatVector, recurrent
import numpy as np
from six.moves import range

from keras import backend


import onehot as oh


data_in_dir = 'data_imported'

class colors:
    ok = '\033[92m'
    fail = '\033[91m'
    close = '\033[0m'

# Parameters for the model and dataset
BATCH_SIZE = 500



print('loading data...')

filename_in = data_in_dir + '/' + 'question.npy'
X = np.load( filename_in )
#X = np.load( 'question.npy' )
filename_in = data_in_dir + '/' + 'answer_onehot.npy'
y = np.load( filename_in )
#y = np.load( 'answer_onehot.npy' )



# Explicitly set apart 10% for validation data that we never train over
split_at = len(X) - len(X) / 10
(X_train, X_val) = (slice_X(X, 0, split_at), slice_X(X, split_at))
(y_train, y_val) = (y[:split_at], y[split_at:])

print(X_train.shape)
print(y_train.shape)
print(X_train.shape[1])
input_dimension = X_train.shape[1]
output_dimension = y_train.shape[1]


print('Build model...')
model = Sequential()


internal_dims=15

model.add( Dense( output_dim=internal_dims, input_dim=input_dimension ) )
#model.add( Activation('sigmoid'))
#model.add( Activation('relu'))
#model.add( Activation('tanh'))
model.add(Activation('softmax'))

model.add( Dense( output_dim=internal_dims) )
model.add( Activation('sigmoid'))
#model.add( Activation('softmax'))

#model.add( Dense( output_dim=92 ) )
#model.add( Activation('relu'))
#model.add( Activation('sigmoid'))

model.add( Dense( output_dim=output_dimension ) )
model.add(Activation('softmax'))
#model.add( Activation('tanh'))
#model.add( Activation('relu'))

#

model.compile(
    loss='mse',
    #loss='categorical_crossentropy',
    #loss='sparse_categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy'])

# Train the model each generation and show predictions against the validation dataset
num_iterations=1000
for iteration in range(1, num_iterations):
    print()
    print('-' * 50)
    print('Iteration', iteration)

    model.fit(X_train, y_train,
              batch_size=BATCH_SIZE,
              nb_epoch=1,
              validation_data=(X_val, y_val)
    )
    #model.fit(X_train, y_train, batch_size=BATCH_SIZE, nb_epoch=1,
    #          validation_data=(X_val, y_val))

    score = model.evaluate(X_val, y_val, batch_size=BATCH_SIZE );
    print( 'score is', score )


    #print( 'summary is', model.summary() )
    #print( 'config is', model.get_config() )
    #print( 'weights are', model.get_weights() )


    

    if iteration == num_iterations - 1:
        ###
        # Select 10 samples from the validation set at random so we can visualize errors
        right = 0;
        wrong = 0;
        for i in range(30):
            ind = np.random.randint(0, len(X_val))
            rowX, rowy = X_val[np.array([ind])], y_val[np.array([ind])]

            print( 'rowX', rowX )
            print( 'rowy', rowy )
            real_class = oh.onehot2int( rowy )
            print( 'real_class', real_class )

            preds  = model.predict( rowX )
            pred_class = oh.onehot2int( preds )
            oh_out    = oh.int2onehot( pred_class, output_dimension )
            print( 'preds', preds )
            print( 'pred_class = ', pred_class, '(', oh_out, ')' )

            preds = model.predict_classes(rowX, verbose=0)
            print( 'predict_classes', preds )

            preds = model.predict_proba( rowX )
            print( 'pred_proba', preds )


            #print('Q', q[::-1] if INVERT else q)
            print('T', real_class)
            print(colors.ok + '☑' + colors.close if real_class == pred_class else colors.fail + '☒' + colors.close, pred_class)
            print('---')

        

        
            #preds = backend.function( model.layers[2].output )
            #print( 'pred', preds )
            print('---')
            





    print( "visual", end="" )
    right =0;

    # confusion matrix
    conf_mat = np.zeros( ( output_dimension, output_dimension ) )
    
    for i in range(100):
        ind = np.random.randint(0, len(X_val))
        rowX, rowy = X_val[np.array([ind])], y_val[np.array([ind])]

        #print( 'rowX', rowX )
        #print( 'rowy', rowy )
        real_class = oh.onehot2int( rowy )
        #print( 'real_class', real_class )

        preds  = model.predict( rowX )
        print( preds )
        pred_class = oh.onehot2int( preds )
        oh_out    = oh.int2onehot( pred_class,  output_dimension )
        #print( 'pred_class = ', pred_class, '(', oh_out, ')' )

        preds = model.predict_classes(rowX, verbose=0)
        #print( 'pred', preds )

        # update confusion matrix
        val = conf_mat[ real_class, pred_class ]
        val = val + 1
        conf_mat[ real_class, pred_class ] = val
        

        #print('T', real_class)
        if real_class == pred_class:
            #print( "fish",end=""),
            print( colors.ok + '☑' + colors.close, end=""),
            right = right + 1
        else:
            #print( "X"),
            print( colors.fail + '☒' + colors.close, end=""),

    ratio = right / float(i)
    print( "ratio: ", ratio )

    print( conf_mat )
    

