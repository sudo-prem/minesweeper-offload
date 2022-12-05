import inspect
import profile
import psutil
import os
import time
import requests
from device_profiler import DeviceProfiler
import pstats
from object_encoder import *
import dis

class TaskProfiler:
    def __init__(self, task):
        self.task = task
        self.CPI = DeviceProfiler().get_local_CPI()
        self.cpu_frequency = DeviceProfiler().get_local_cpu_frequency()
        self.instruction_count = -1.0

    def get_estimated_time(self, task):
        time = pstats.Stats(task).total_tt
        return time

    # def get_instruction_count_sc(self):
    #     if self.instruction_count != -1.0:
    #         return self.instruction_count

    #     # Estimated time for task execution
    #     time = get_estimated_time(self.task)
    #     try:
    #         self.instruction_count = (time * self.cpu_frequency + 1) // self.CPI
    #         print("SC:" , self.instruction_count)
    #     except ZeroDivisionError:
    #         print("CPI has not been set properly!")
    #         exit()
    #     return self.instruction_count

    def get_instruction_count(self):
     
        ic = dis.get_instructions(self.task)
        count=0
        for i in ic:
            count+=1
        self.instruction_count = count
        return self.instruction_count



if __name__ == '__main__':
    def test():
        s1 = 'hello'
        s2 = 'hell'
        n = 5
        m = 4
        # using dp fill the table
        dp = [[0 for i in range(m + 1)] for j in range(n + 1)]

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[n][m]

    task_profiler = TaskProfiler(test)
    # print(task_profiler.get_instruction_count())
    # print(task_profiler.get_instruction_count_sc())
