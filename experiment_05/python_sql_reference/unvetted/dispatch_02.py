
import json
import db_read
import os
import subprocess
import time
import s3_uploader_02
import base64

server_addr = "https://safetymaneatsfriedrice-dev.s3.amazonaws.com/"

# send response
#{
#   "id":1932,
#   "result":{
#             "file":"<file name>",
#             "url":"<S3 URL>",
#             "sha256":"<base64 sha256 of archive>"
#          }
#}
def make_response_success( req_id, archive_filename, server_addr, hashval ):
    resp = {}
    resp[ "id" ] = str( req_id )

    result = {}
    result[ "file" ]   = archive_filename
    result[ "url"  ]   = server_addr + archive_filename
    result[ "sha256" ] = hashval

    resp[ "result" ] = result
    print( "will send this result:" )
    print( resp )

    return resp

#{
#   "id":1932,
#   "error":{
#      "code":400,
#      "message":"error setting pin mode"
#   }
#}
def make_response_fail( req_id ):
    resp = {}
    resp[ "id" ] = str( req_id )   

    error = {}
    error[ "code"    ] = str( 400 )
    error[ "message" ] = "No files matching range found"
    resp[ "error" ] = error
    print( "will send this result: ")
    print( resp )
    
    return resp

def handle_request_audio_get_range( req_data, rec_data_path ):
    req_id = req_data[ "id" ]
    print( "Will now handle audio.getrange(), req_id: ", req_id )

    # get params
    time_start = int( req_data["params"]["startTime"] )
    time_stop  = int( req_data["params"]["stopTime"] )
    s3_bucket  = req_data["params"]["bucket"]

    # look for that audio
    #    import pdb; pdb.set_trace()
    print( "my time_start and _stop are: ", time_start, time_stop )
    
    ret_val = db_read.get_range( time_start, time_stop )

    # create the .zip archive
    row_count = 0
    archive_filename = "audio_req_" + str( time_start) + "_" + str( time_stop ) + ".zip";
    for row in ret_val:
        print( row )
        sound_filename = rec_data_path + "/" + row[0] + "/" + "rec.wav"
        print( sound_filename )
        cmd = "zip " + archive_filename + " " + sound_filename
        print( cmd )
        os.system( cmd )
        row_count = row_count + 1
    print( "Found " + str( row_count ) + " rows." )
    
    if row_count > 0:        
        # calculate SHA256 hash
        hashproc = subprocess.Popen( ['sha256sum', archive_filename ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = hashproc.communicate()
        #time.sleep(1)
        out2 = output.decode( 'utf-8' )
        err2 = err.decode( 'utf-8' )
        ret2 = str( hashproc.returncode )
        print( "output:" + out2 )
        print( type(out2) )
        print( "err: " + err2 )
        print( "retcode: " + ret2 )
    
        hashret = out2.split( ' ' )
        hashval = hashret[ 0 ]   # these are hex values in asci
        hashval_bytes = bytes.fromhex( hashval )
        hashval_b64 = base64.b64encode( hashval_bytes )
        hashval_64 = hashval_b64.decode("ascii")
        print( hashval )
        print( hashval_64 )

        print( "Uploading to S3 bucket" )
        access_key = os.environ.get( 'AWS_ACCESS_KEY_ID' )
        secret_key = os.environ.get( 'AWS_SECRET_ACCESS_KEY' )

        aaa = s3_uploader_02.upload_file_S3( archive_filename, s3_bucket, access_key, secret_key )
        print( aaa )
        resp = make_response_success( req_id, archive_filename, server_addr, hashval_64 )    

        # clean up
        os.remove( archive_filename )
    else:
        resp = make_response_fail( req_id )

    return resp
    
def handle_result( req_id, req_data ):
    
    resp = {}
    resp[ "id" ] = str( req_id );
    return resp
    
    

def handle_request_result( data ):
    result_id = data["id"]
    print( "got a result: ", result_id )
    resp = handle_result( result_id, data );
    return resp

    

    



    

        


    
