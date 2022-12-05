from xmlrpc.server import SimpleXMLRPCServer
from json import loads, JSONEncoder, dumps
import random
import pickle
from base64 import b64decode, b64encode

import sys
sys.path.append('../offload')

from device_profiler import *
from mul_remote import *
from object_encoder import ObjectEncoder, as_python_object

# Functions to register
local_frequency = DeviceProfiler().get_local_cpu_frequency
local_CPI = DeviceProfiler().get_local_CPI


def server_metrics():
    return local_frequency(), local_CPI()


def Matrix_Mul_Remote(code_sync):

    try:
        code_sync_remote = loads(code_sync, object_hook=as_python_object)
    except:
        print("Error while decoding the object obtained from the UE")
        exit()

    print("*** Executed Remotely ***")
    remoteClassVar = MatrixMultiplication(2)
    keys = locals()['code_sync_remote'].keys()
    values = locals()['code_sync_remote'].values()
    for key, val in zip(keys, values):
        setattr(remoteClassVar, key, val)

    result = remoteClassVar.standard_matrix_product()

    codeSyncDict = remoteClassVar.__dict__

    codeSyncDict['retVal'] = result
    # print(codeSyncDict)
    try:
        res = dumps(codeSyncDict, cls=ObjectEncoder)
        return res
    except:
        print("Error while encoding the object in the server")
        exit()


if __name__ == '__main__':
    try:
        server = SimpleXMLRPCServer(("", 8000))
    except:
        print("Error in starting remote server!")
        exit()
    print("Listening on port 8000...")
    server.register_function(local_frequency, "local_frequency")
    server.register_function(local_CPI, "local_CPI")
    server.register_function(Matrix_Mul_Remote, "Matrix_Mul_Remote")
    server.register_function(server_metrics, "server_metrics")
    server.serve_forever()
