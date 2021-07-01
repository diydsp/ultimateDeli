

import argparse

parser = argparse.ArgumentParser( description='control learner' )

parser.add_argument( '--iter',
                     dest='num_iterations',
                     help='number of iterations to run' )

parser.add_argument( '--ratio_select',
                     dest='ratio_select',
                     help='select which ratio to train on' )

if __name__ == '__main__':
    args = parser.parse_args()

    print args.num_iterations
    print args.ratio_select

    

