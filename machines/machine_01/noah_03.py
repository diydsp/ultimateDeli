# -*- coding: utf-8 -*-
'''predict weekly performance of equities from features
this one turns the requested output feature into onehot class
'''

from __future__ import print_function

import numpy as np

from keras.models import Sequential
from keras.engine.training import slice_X
from keras.layers import Activation, TimeDistributed, Dense, RepeatVector, recurrent
from keras.optimizers import SGD

import onehot as oh


data_in_dir = 'data_imported'

class colors:
    ok = '\033[92m'
    fail = '\033[91m'
    close = '\033[0m'

# Parameters for the model and dataset
BATCH_SIZE = 500
internal_dims = 5   # number of layers


print('loading data...')
filename_in = data_in_dir + '/' + 'question.npy'
X = np.load( filename_in )
filename_in = data_in_dir + '/' + 'answer_onehot.npy'
#filename_in = data_in_dir + '/' + 'answer.npy'
y = np.load( filename_in )

print("shapes")
print(X.shape)
print(y.shape)

# Explicitly set apart 10% for validation data that we never train over
split_at = len(X) - len(X) / 10
(X_train, X_val) = (slice_X(X, 0, split_at), slice_X(X, split_at))
(y_train, y_val) = (y[:split_at], y[split_at:])
print("X_train.shape")
print(X_train.shape)
print("y_train.shape")
print(y_train.shape)
print("X_train.shape[1]")
print(X_train.shape[1])
input_dimension = X_train.shape[1]
output_dimension = y_train.shape[1]   
#output_dimension = 1   # used with single-dimensional answer array


print('Build model...')
model = Sequential()

model.add( Dense( output_dim=internal_dims, input_dim=input_dimension ) )
#model.add( Activation('sigmoid'))
#model.add( Activation('relu'))
#model.add( Activation('tanh'))
model.add(Activation('softmax'))

#model.add( Dense( output_dim=internal_dims) )
#model.add( Activation('softmax'))
#model.add( Activation('sigmoid'))

#model.add( Dense( output_dim=92 ) )
#model.add( Activation('relu'))
#model.add( Activation('sigmoid'))

model.add( Dense( output_dim=output_dimension ) )
model.add(Activation('softmax'))
#model.add( Activation('tanh'))
#model.add( Activation('relu'))

#model.add( Dense( output_dim=output_dimension ) )
#model.add(Activation('softmax'))

sgd = SGD( lr = 0.1,
           decay=1e-6,
           momentum=0.9,
           nesterov=True
)

model.compile(
    loss='mse',
    #loss='categorical_crossentropy',
    #loss='sparse_categorical_crossentropy',
    optimizer='adam',
    #optimizer='adadelta',
    #optimizer='rmsprop',
    #optimizer=sgd,
    #metrics=['accuracy']
)




def confus_mat_calc():
    print( "visual", end="" )
    right =0;

    # make confusion matrix
    conf_mat = np.zeros( ( output_dimension, output_dimension ) )

    for i in range(100):
        #print( i, ")", end="" )

        ind = np.random.randint(0, len(X_val))
        #print( ind, "#", end="" )
        rowX, rowy = X_val[np.array([ind])], y_val[np.array([ind])]

        #print( 'rowX', rowX )
        #print( 'rowy', rowy )
        real_class = oh.onehot2int( rowy )
        #print( 'real_class', real_class )

        preds  = model.predict( rowX )
        #preds  = model.predict_classes( rowX, verbose=0 )
        #preds  = model.predict_proba( rowX )
        #pred_cls = model.predict_classes(rowX, verbose=0)
        #print( 'pred_cls', pred_cls )

        print( "hey", preds, "fish" )

        pred_class = oh.onehot2int( preds )
        oh_out    = oh.int2onehot( pred_class,  output_dimension )
        #print( 'pred_class = ', pred_class, '(', oh_out, ')' )


        # update confusion matrix
        val = conf_mat[ real_class, pred_class ]
        val = val + 1
        conf_mat[ real_class, pred_class ] = val
        

        #print('T', real_class)
        if real_class == pred_class:
            #print( "fish",end=""),
            print( colors.ok + '???' + colors.close, end=""),
            right = right + 1
        else:
            #print( "X"),
            print( colors.fail + '???' + colors.close, end=""),

    ratio = right / float(i)
    print( "ratio: ", ratio )

    print( conf_mat )
    


def preview_visualize():

    # make confusion matrix
    conf_mat = np.zeros( ( output_dimension, output_dimension ) )

    ###
    # Select 10 samples from the validation set at random so we can visualize errors
    right = 0;
    for i in range(50):
        #print( "Hello its me", i, end="" )
        
        ind = np.random.randint(0, len(X_val))
        rowX, rowy = X_val[np.array([ind])], y_val[np.array([ind])]
        
        #print( 'rowX', rowX )
        #print( 'rowy', rowy )
        real_class = oh.onehot2int( rowy )
        #print( 'real_class', real_class )
        
        #print
        #print( "type( rowX )" )
        #print( type( rowX ) )
        #print( rowX.shape )
        
        preds  = model.predict( rowX, verbose = 0 )
        #print( rowX[ 0 ][ 0 ], rowX[ 0 ][ 1 ], rowX[ 0 ][ 2 ], rowX[ 0 ][ 3 ] )
        print( 'preds', preds, end="" )
        
        pred_class = oh.onehot2int( preds )
        #oh_out    = oh.int2onehot( pred_class, output_dimension )
        #print( 'pred_class = ', pred_class, '(', oh_out, ')' )
        
        preds = model.predict_classes(rowX, verbose=0)
        #print( 'predict_classes', preds )
        
        pred_probas = model.predict_proba( rowX, verbose = 0 )
        #print( 'pred_probas', pred_probas )
        
        
        #print( model.predict( np.array( [ [ 30, 40, 20, 25 ] ] ) ) )
        #print( model.predict( np.array( [ [ 9, 8, 7, 6 ] ] ) ) )
        #print( model.predict( np.array( [ [ 1, 2, 3, 4 ] ] ) ) )
        #print( model.predict( np.array( [ [ 9, 1, 8, 2 ] ] ) ) )
        
        if real_class == pred_class:
            right = right + 1
            
        # update confusion matrix
        val = conf_mat[ real_class, pred_class ]
        val = val + 1
        conf_mat[ real_class, pred_class ] = val
        
                
        #print('Q', q[::-1] if INVERT else q)
        print(colors.ok + '???' + colors.close if real_class == pred_class else colors.fail + '???' + colors.close, end="" )
        print('T', real_class, pred_class )
        #print(colors.ok + '???' + colors.close if real_class == pred_class else colors.fail + '???' + colors.close, pred_class)
        #print('---')

    ratio = right / float(i)
    print( "ratio: ", ratio )
            
    print( conf_mat )
    
# Train the model each generation and show predictions against the validation dataset
num_iterations=50
for iteration in range(1, num_iterations):
    print()
    print('-' * 50)
    print('Iteration', iteration)

    model.fit(X_train, y_train,
              batch_size=BATCH_SIZE,
              nb_epoch=400,
              verbose=0,
              validation_data=(X_val, y_val)
    )
    #model.fit(X_train, y_train, batch_size=BATCH_SIZE, nb_epoch=1,
    #          validation_data=(X_val, y_val))

    score = model.evaluate(X_val, y_val, batch_size=BATCH_SIZE );
    print( 'score is', score )


    #print( 'summary is', model.summary() )
    #print( 'config is', model.get_config() )
    #print( 'weights are', model.get_weights() )


    #confus_mat_calc()


    #print( model.predict( np.array( [ [ 5, 6, 7, 8 ] ] ) ) )
    #print( model.predict( np.array( [ [ 9, 8, 7, 6 ] ] ) ) )
    #print( model.predict( np.array( [ [ 1, 2, 3, 4 ] ] ) ) )
    #print( model.predict( np.array( [ [ 9, 1, 8, 2 ] ] ) ) )
    
    #print( model.predict( np.array( [ [ 5, 6, 7, 8, 9 ] ] ) ) )
    #print( model.predict( np.array( [ [ 9, 8, 7, 6, 5 ] ] ) ) )
    #print( model.predict( np.array( [ [ 5, 6, 7, 8, 9000 ] ] ) ) )
    #print( model.predict( np.array( [ [ 9, 8, 7, 6, 5700 ] ] ) ) )
    

    #if iteration == num_iterations - 1:
    preview_visualize()

        

        
            








