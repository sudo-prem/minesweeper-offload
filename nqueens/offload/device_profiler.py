import psutil
from offload.object_encoder import *
import time
from xmlrpc.client import ServerProxy
from constants import *


class DeviceProfiler:

    def __init__(self):
        self.server = None
        self.CPI = None
        self.frequency = None

    def connect_to_server(self):
        if self.server != None:
            return
        url = Constants.getInstance().SERVER_URL
        try:
            self.server = ServerProxy(url)
        except:
            print("Error connecting to the remote server!")
            exit()

    def get_remote_cpu_frequency(self):
        self.connect_to_server()
        cpu_frequency = self.server.local_frequency()
        return cpu_frequency

    def get_remote_CPI(self):
        self.connect_to_server()
        CPI = self.server.local_CPI()
        return CPI

    # Returns in hertz
    def get_local_cpu_frequency(self):
        # cpu_info = cpuinfo.get_cpu_info()
        self.frequency = psutil.cpu_freq().current
        return self.frequency

    def swap(self):
        x = 9342
        y = 3452

        x = x ^ y
        y = x ^ y
        x = x ^ y


    def get_local_CPI(self):
        if self.CPI != None:
            return self.CPI

        IC = 3
        total_CPI = 0
        
        for i in range(7):
            task = self.swap
            
            time_taken = get_estimated_time(task)
            freq = self.get_local_cpu_frequency()

            # first 1000 - converting seconds to milli seconds
            # second 1000 - converting hertz to milli seconds
            curr = (time_taken * 1000) / (freq * IC) * 1000
            total_CPI += curr

        self.CPI = round(total_CPI / 7, 1)
        return self.CPI


if __name__ == '__main__':
    device_profiler = DeviceProfiler()
    print(device_profiler.get_local_cpu_frequency())
    print(device_profiler.get_local_CPI())
    print(device_profiler.get_remote_cpu_frequency())
    print(device_profiler.get_remote_CPI())
