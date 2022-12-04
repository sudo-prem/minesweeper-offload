from base64 import b64encode, b64decode
from json import dumps, loads, JSONEncoder, JSONDecoder
from offload.device_profiler import DeviceProfiler
import xmlrpc.client
from offload.object_encoder import ObjectEncoder, as_python_object

from offload.profiler import *
import sys
from constants import *

local_count=0
remote_count=0

def print_counts():
    global local_count, remote_count
    print("Local Count: ", local_count)
    print("Remote Count: ", remote_count)

def offmat(task, code_sync_obj):
    global local_count, remote_count

    obj = dumps(code_sync_obj, cls=ObjectEncoder)
    # TODO: check units
    data_size = sys.getsizeof(obj) / 1024

    profiler = Profiler(task=task, data_size=data_size)

    local_exec_cost = profiler.get_local_execution_cost()
    local_exec_cost = round(local_exec_cost, 3)
    remote_exec_cost = profiler.get_remote_execution_cost()
    remote_exec_cost = round(remote_exec_cost, 3)

    print("Local Execution Cost : ", local_exec_cost, "ms")
    print("Remote Execution Cost: ", remote_exec_cost, "ms")

    flag = 0

    if local_exec_cost < remote_exec_cost:
        local_count += 1
        print("Local Execution")
        print_counts()
        return False
    else:
        print("Remote Execution")
        try:
            server = xmlrpc.client.ServerProxy(
                Constants.getInstance().SERVER_URL)
        except:
            print("Error in connecting to the remote server!")
            local_count += 1
            print("Local Execution")
            print_counts()
            # self.conclusion()
            flag = 1
            return False
        if(flag == 0):
            remote_count += 1
            csRemote = server.Matrix_Mul_Remote(obj)
            try:
                csResult = loads(csRemote, object_hook=as_python_object)
            except:
                print("Error in loading the object from the server!")
                exit()
                
            print_counts()
            return csResult

