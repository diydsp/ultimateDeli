#!/usr/bin/python
# -*- coding: utf-8 -*-

# basic learning program that learns one-hot "answers" to "question" vectors


'''candlestick predictor
'''

from __future__ import print_function

# python/environment
import argparse

# math libs
import numpy as np

from keras.models import Sequential
from keras.engine.training import slice_X
from keras.layers import Activation, TimeDistributed, Dense, RepeatVector, recurrent
from keras.optimizers import SGD

from sklearn.utils import shuffle

# my stuff
import onehot as oh


results_dir = 'tmp'

# command line args/control parameters
parser = argparse.ArgumentParser( description='control learner' )

parser.add_argument( '--ticker',
                     dest='ticker',
                     help='ticker symbol, e.g. INSY' )

parser.add_argument( '--level',
                     dest='level',
                     help='level, e.g. m1_100' )

parser.add_argument( '--iter',
                     dest='num_iterations',
                     help='number of iterations to run' )

parser.add_argument( '--dims_internal',
                     dest='internal_dims',
                     help='internal dimensions of network' )

parser.add_argument( '--extra_layers',
                     dest='extra_layers',
                     help='extra layers of network, 1 layer is default' )

visualize_validation = 0

if __name__ == '__main__':
    args = parser.parse_args()

    print( 'Using num_iterations', args.num_iterations )
    print( 'Using internal_nums', args.internal_dims )



data_in_dir = 'data_imported'


# Parameters for the model and dataset
epoch_size     = 200
num_iterations = int( args.num_iterations ) # typical 10 through 200
internal_dims  = int( args.internal_dims )  # typical 4 through 20
extra_layers   = int( args.extra_layers  )  # typical 2 through 5
BATCH_SIZE     = 500
visualization_length = 100;


# load data
print('loading data...')
class_dir              = 'level_list/' + args.level + '/tick_list/' + args.ticker + '/class/'
features_dir           = class_dir + 'features/'
model_dir              = class_dir + 'models/'
filename_question      = features_dir + 'question.npy'
filename_answer_onehot = features_dir + 'answer_onehot.npy'
filename_results       = model_dir + 'results_out.txt'
filename_model         = model_dir + 'model.h5'

X = np.load( filename_question )
y = np.load( filename_answer_onehot )

#filename_in = data_in_dir + '/' + 'question.npy'
#X = np.load( filename_in )
#filename_in = data_in_dir + '/' + 'answer_onehot.npy'
##filename_in = data_in_dir + '/' + 'answer.npy'
#y = np.load( filename_in )

print("shapes")
print(X.shape)
print(y.shape)

# must shuffle because partitioning for validation based on
# final N values only gets most recent values in time
X, y = shuffle( X, y, random_state = 0 )


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

# initial layer
model.add( Dense( output_dim=internal_dims, input_dim=input_dimension ) )
model.add(Activation('softmax'))
#model.add( Activation('sigmoid'))
#model.add( Activation('relu'))
#model.add( Activation('tanh'))

# intermediate layers
for layers_count in range( extra_layers ):
    model.add( Dense( output_dim=internal_dims) )
    model.add( Activation('softmax'))

# final layer
model.add( Dense( output_dim=output_dimension ) )
model.add(Activation('softmax'))

# compile model
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


# log results as it trains
#results_file_out = results_dir + '/' + 'results_out.txt'
results_out = open( filename_results, 'w' )


class colors:
    ok = '\033[92m'
    fail = '\033[91m'
    close = '\033[0m'



# make confusion matrix
conf_mat = np.zeros( ( output_dimension, output_dimension ) )
ratio    = 0
cf_score = 0

def preview_visualize():

    # make confusion matrix
    conf_mat.fill( 0 )

    # Select samples from the validation set at random so we can visualize errors
    right = 0;
    for i in range( visualization_length ):
        #print( "Hello its me", i, end="" )
        
        #ind = np.random.randint(0, len(X))
        ind = np.random.randint(0, len(X_val))
        #ind = i   # TEMPORARY
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
        if visualize_validation == 1:
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
        
        if visualize_validation == 1:
            print(colors.ok + '☑' + colors.close if real_class == pred_class else colors.fail + '☒' + colors.close, end="" )
            print('T', real_class, pred_class )

    ratio = right / float(i)
    print( "ratio: ", ratio )
            
    print( conf_mat )

    # evaluate conf_mat
    cf_score  = conf_mat[ 0 ][ 0 ] + conf_mat[ 1 ][ 1 ] + conf_mat[ 2 ][ 2 ]
    cf_score -= conf_mat[ 0 ][ 2 ] + conf_mat[ 2 ][ 0 ]
    print( 'cf_score, ' + str( cf_score ) )    
    
    # save results to file
    results_out.write( str( conf_mat ) )
    results_out.write( '\n' )
    results_out.write( 'cf_score, ' + str( cf_score ) )
    results_out.write( '\n' )
    results_out.write( 'ratio, '    + str( ratio ) )
    results_out.write( '\n' )
    
    
    
# Train the model each generation and show predictions against the validation dataset
for iteration in range(1, 1 + num_iterations):
    print()
    print('-' * 50)
    print('Iteration', iteration)

    model.fit(X_train, y_train,
              batch_size=BATCH_SIZE,
              nb_epoch= epoch_size,
              verbose=0,
              validation_data=(X_val, y_val)
    )

    # save progress
    model.save( filename_model )
    
    score = model.evaluate(X_val, y_val, batch_size=BATCH_SIZE );
    print( 'score is', score )


    #print( 'summary is', model.summary() )
    #print( 'config is', model.get_config() )
    #print( 'weights are', model.get_weights() )

    #print( model.predict( np.array( [ [ 5, 6, 7, 8 ] ] ) ) )
    #print( model.predict( np.array( [ [ 9, 8, 7, 6 ] ] ) ) )
    #print( model.predict( np.array( [ [ 1, 2, 3, 4 ] ] ) ) )
    #print( model.predict( np.array( [ [ 9, 1, 8, 2 ] ] ) ) )
    
    #print( model.predict( np.array( [ [ 5, 6, 7, 8, 9 ] ] ) ) )
    #print( model.predict( np.array( [ [ 9, 8, 7, 6, 5 ] ] ) ) )
    #print( model.predict( np.array( [ [ 5, 6, 7, 8, 9000 ] ] ) ) )
    #print( model.predict( np.array( [ [ 9, 8, 7, 6, 5700 ] ] ) ) )
    

    preview_visualize()
    
        


            








