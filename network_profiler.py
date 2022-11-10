import psutil
import os
import time
import sys
import requests
from constants import *

class NetworkProfiler:

    # Current Network usage Percentage
    def get_network_usage_percentage(self):
        net_usage = psutil.net_io_counters(pernic=False)
        net_usage_percentage = net_usage[2] / net_usage[0]
        return net_usage_percentage

    # Network cost for 1 byte
    def get_rtt(self):
        url = Constants.getInstance().SERVER_URL
        # url = "https://google.com/"
        start_time = time.time()
        try:
            response = requests.get(url)
        except:
            print("Network Error! GET request not successful")
            sys.exit()
        
        res_size = sys.getsizeof(response)
        end_time = time.time()
        rtt = (((end_time - start_time) * 1000)) / res_size
        return rtt

    # Network usage Percentage for a given time
    def get_network_usage_percentage_for_time(self, time):
        start_time = time.time()
        net_usage = psutil.net_io_counters(pernic=False)
        while time.time() - start_time < time:
            pass
        net_usage = psutil.net_io_counters(pernic=False)
        net_usage_percentage = net_usage[2] / net_usage[0]
        return net_usage_percentage


if __name__ == '__main__':
    network_profiler = NetworkProfiler()
    # print(round(network_profiler.get_network_usage_percentage(), 5))
    print(round(network_profiler.get_rtt(), 5))
