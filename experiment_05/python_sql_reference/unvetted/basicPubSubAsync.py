from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import os
import base64
import json
import pydb_intf
import sys
import datetime as dt

rec_data_path = "/data/rec_data"

# General message notification callback
def customOnMessage(message):
    print("--------------")
    print("From topic: ")
    print(message.topic)
    print("Received message: ")
    print(message.payload)

    # sneak preview of message type
    print( "json data:" )
    data = json.loads( message.payload.decode("utf-8") )
    print( data )

    # determine if msg destined for us
    topic_fields = message.topic.split( '/' )
    print( "topic_fields: ", end='')
    print( topic_fields )
    if( topic_fields[ 0 ] == 'v1' and
        topic_fields[ 1 ] == 'devices' and
        topic_fields[ 2 ] == my_device_name and
        topic_fields[ 3 ] == 'rpc' ):
        #topic_fields[ 4 ] == 'request' ):
        
        # dispatch it
        if "method" in data:
            if data[ "method" ] == "Audio.GetRange":

                if args.start_time and args.end_time:
                    print( "won't handle it because I am a request maker." )
                else:
                    ret_data = pydb_intf.handle_request_audio_get_range( data, rec_data_path )
                    print( "ret_data from audio.getRange: ", ret_data )
                    if "result" in ret_data:
                        print( "request handled.  will now transmit result" )
                        resp_json = json.dumps( ret_data )
                        print( resp_json )
                    
                        # transmit result
                        topic_resp = message.topic.replace( "request", "response" )
                        print( "Made topic_resp: " + topic_resp )
                        myAWSIoTMQTTClient.publishAsync(topic_resp, resp_json, 1, ackCallback=customPubackCallback)

        elif "result" in data:
            ret_data = pydb_intf.handle_request_result( data )
            print( "ret_data from audio.getRange: ", ret_data )  
            print( "and we're done!" )
    else:
        print( "not destined for me" )


# Suback callback
def customSubackCallback(mid, data):
    print("Received SUBACK packet id: ", end='')
    print(mid, end=', ' )
    print("Granted QoS: ", end='' )
    print(data)


# Puback callback
def customPubackCallback(mid):
    print("Received PUBACK packet id: ")
    print(mid)
    print("++++++++++++++\n\n")


# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-tb", "--topic_base", action="store", dest="topic_base", default="sdk/test/Python", help="Targeted topic")
parser.add_argument("-m", "--make-request", action="store", dest="request_string", help="Request string, e.g. 2019_05_01_12_30_59" )
parser.add_argument("-ek", "--environment-keys", action="store", dest="environment_keys", help="get security keys from environment variables" )
parser.add_argument("-st", "--start-time", action="store", dest="start_time", help="Start time, e.g. 2010_07_04_04_30_06" )
parser.add_argument("-et", "--end-time", action="store", dest="end_time", help="End time, e.g. 2010_07_04_10_56_46" )

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
port = args.port
useWebsocket = args.useWebsocket
clientId = args.clientId
topic_base = args.topic_base

my_device_name = os.environ.get( "BALENA_DEVICE_NAME_AT_INIT" )

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Port defaults
if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
    port = 443
if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
    port = 8883

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
#logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

def environ_to_file( env_var_name, filename ):
    var_val = os.environ.get( env_var_name )
    decoded = base64.b64decode( var_val ).decode( "utf-8" )
    #print( decoded )
    #print( filename )
    #print( var_val )
    fhand = open( filename, "w" )
    fhand.write( decoded )
    fhand.close
    

    
# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)

    # pass security from env variables to file system
    if args.environment_keys:
        dir_location = "security"
        if not os.path.isdir( dir_location ):
            os.mkdir( dir_location )
        privateKeyPath = dir_location + "/" + "priv_key.pem.txt"
        environ_to_file( 'MQTT_PRIV_KEY', privateKeyPath )

        certificatePath = dir_location + "/" + "cert.pem.txt"
        environ_to_file( 'MQTT_CERT'    , certificatePath )
    
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
    # delete after connecting
    
# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.onMessage = customOnMessage

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
# Note that we are not putting a message callback here. We are using the general message notification callback.

if not (args.start_time and args.end_time):
#if True:
    topic_sub = "v1/devices/" + my_device_name + "/rpc/request/+"
    #print( "made topic_sub: " + topic_sub )
else:
    topic_sub = "v1/devices/" + my_device_name + "/rpc/response/+"
        
print( "subbing to topic:" + topic_sub )
myAWSIoTMQTTClient.subscribeAsync( topic_sub, 1, ackCallback=customSubackCallback)
time.sleep( 2 )

if args.start_time and args.end_time:

    print("Will make a request of type: Audio.GetRange" )

    #{
    #    "id":1932,
    #    "method":"Audio.GetRange",
    #    "params":{
    #        "startTime":1588906983,
    #        "stopTime":15889012345,
    #        "bucket":"<s3 bucket location>"
    #    }
    #}

    req = {}
    req_id = int( dt.datetime.now().timestamp() )  # timestamp is date
    req[ "id"     ] = str( req_id );
    req[ "method" ] = "Audio.GetRange";
    params = {}
    params[ "startTime" ] = str( args.start_time )
    params[ "stopTime"  ] = str( args.end_time )
    params[ "bucket"    ] = "safetymaneatsfriedrice-dev"    
    req[ "params" ] = params;
    req_json = json.dumps( req )

    print( 'Generated this json:' )
    print( req_json )
    topic_req = topic_base + "/" + str( req_id )
    myAWSIoTMQTTClient.publishAsync( topic_req, req_json, 1, ackCallback=customPubackCallback)

        
# Publish to the same topic in a loop forever
loopCount = 0

while True:
    loopCount += 1
    time.sleep(1)

