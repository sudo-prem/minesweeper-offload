from base64 import b64encode, b64decode
from json import dumps, loads, JSONEncoder, JSONDecoder
from device_profiler import DeviceProfiler
import xmlrpc.client
from object_encoder import ObjectEncoder, as_python_object

from profiler import *
import sys
from constants import *

local_count=0
remote_count=0

def print_counts():
    global local_count, remote_count
    print("Local Count: ", local_count)
    print("Remote Count: ", remote_count)
    print()

def offmat(task, code_sync_obj, code_for_ic):
    global local_count, remote_count

    # returns False as the Offloading decision to the caller
    def execute_local():
        global local_count
        local_count+=1
        print("***Local Execution***")
        print_counts()
        return False
    
    #Returns server response object in case of success, False otherwise
    def execute_remote():
        global remote_count
        remote_count+=1
        print("***Remote Execution***")
        try:
            server = xmlrpc.client.ServerProxy(
                Constants.getInstance().SERVER_URL)
                
            csRemote = server.Remote_Method(obj)
            # csRemote = server.NQueens_Remote(obj)

            try:
                csResult = loads(csRemote, object_hook=as_python_object)
                print_counts()
                return csResult
            except:
                print("Error in loading the object from the server!")
                return False
        except:
            print("Error in connecting to the remote server!")
            return False
        
    obj = dumps(code_sync_obj, cls=ObjectEncoder)
    # TODO: check units
    data_size = sys.getsizeof(obj) / 1024

    profiler = Profiler(task=task, data_size=data_size, code_for_ic=code_for_ic)

    local_exec_cost = profiler.get_local_execution_cost()
    local_exec_cost = round(local_exec_cost, 3)
    remote_exec_cost = profiler.get_remote_execution_cost()
    remote_exec_cost = round(remote_exec_cost, 3)

    print("Local Execution Cost : ", local_exec_cost, "ms")
    print("Remote Execution Cost: ", remote_exec_cost, "ms")
    print()

    #Check if the battery is sufficient to execute the task locally
    battery_status = profiler.batteryTracker.get_battery_status()
    local_energy_cost = profiler.get_local_energy_consumption()
    print("Local Energy Cost: ", local_energy_cost, "mwh")
    print("Battery Level: ", battery_status['RemainingCapacity'], "mwh")


    #Compare costs and execute locally or remotely
    if local_exec_cost < remote_exec_cost:

        
        if battery_status['RemainingCapacity'] > local_energy_cost:
            
            return execute_local()

        # If the battery is not sufficient offload the task to the remote server
        else:
            print("**Battery is not sufficient to execute the task locally!**")
            result = execute_remote()
            if result == False:
                print("Execution Failed!")
                exit(1)
            else:
                return result
    else:
        
        result = execute_remote()
        if result == False:
            # Try executing the task locally
            if battery_status['RemainingCapacity'] > local_energy_cost:
                return execute_local()
            
            else:
                print("Low Battery - Execution Failed!")
                exit(1)
        else:
            return result

