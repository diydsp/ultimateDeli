
import os
import json

# read/write model parameters for the level (and model)

def filename_get( level_name, model_name):

    # Level
    path_level = "level_list/" + level_name;
    if not os.path.exists( path_level ):
        print "can't find path_level: " + path_level
        sys.exit()

    # Params
    params_dir = "level_list/" + level_name + "/params/" + model_name +"/";
    if not os.path.exists( params_dir ):
        print "can't find params_dir: " + params_dir
        sys.exit()

    print "using params_dir: " + params_dir

    # read from file
    filename_in = params_dir + "params.json"

    return filename_in



def read( filename_in ):

    with open( filename_in, 'r') as fff:
        params = json.load( fff )

    return params

def write( params_file, args ):

    # Build internal structure
    params={}
    params[ 'dims_internal' ] = args.dims_internal;
    params[ 'extra_layers'  ] = args.extra_layers;
    params[ 'ratio_select'  ] = args.ratio_select;

    json_str = json.dumps( params )
    print json_str

    #json_str = '{ "iterations": 5, "internal_dims":3, "extra_layers":5 }'

    # check it
    parsed = json.loads( json_str )
    print parsed[ 'dims_internal' ]

    # write to a file
    #file_out_name = params_dir + "params.json"
    print "writing to: " + params_file
    with open( params_file, 'w') as fff:
        json.dump( params, fff )
