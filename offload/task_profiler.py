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
    def __init__(self, task, code_for_ic):
        self.task = task
        self.CPI = DeviceProfiler().get_local_CPI()
        self.cpu_frequency = DeviceProfiler().get_local_cpu_frequency()
        self.instruction_count = -1.0
        self.code_for_ic = code_for_ic

    def get_estimated_time(self, task):
        time = pstats.Stats(task).total_tt
        return time

    def get_ic(self, instructions):
        i = 0
        length = len(instructions)
        ic = length
        forIterDict = {}  # stores the offset of the FOR_ITER instruction and the ending offset
        forIterIterator = {}  # stores the offset of the FOR_ITER instruction and the iterator
        while (i < length):
            if instructions[i].opname == 'FOR_ITER':
                forIterDict[instructions[i].offset] = instructions[i].argval - 2
                j = i - 1
                while (instructions[j].opname != 'LOAD_ATTR' and instructions[j].opname != 'LOAD_CONST' and instructions[j].opname != 'LOAD_FAST' and instructions[j].opname != 'LOAD_DEREF'):
                    j -= 1
                if (instructions[j].opname == 'LOAD_ATTR' or instructions[j].opname == 'LOAD_FAST' or instructions[j].opname == 'LOAD_DEREF'):
                    if (instructions[j].argval == '__dict__'):
                        value = self.code_for_ic['dict']
                    else:
                        value = self.code_for_ic[instructions[j].argval]
                    if (isinstance(value, int) or isinstance(value, float)):
                        forIterIterator[instructions[i].offset] = value
                    else:
                        forIterIterator[instructions[i].offset] = len(value)
                elif (instructions[j].opname == 'LOAD_CONST'):
                    forIterIterator[instructions[i].offset] = instructions[j].argval

            i += 1

        flag = 0
        print(forIterDict)
        print(forIterIterator)
        for offset, endingoffset in forIterDict.items():
            if (flag == 0):
                ins_count = (endingoffset - offset) / 2
                multiplier = forIterIterator[offset]
                for key in forIterDict.keys():
                    if (key > offset and key <= endingoffset):
                        multiplier *= forIterIterator[key]
                        flag += 1
                ic += (ins_count * multiplier)
            else:
                flag -= 1
        return ic

    def get_instruction_count(self):

        instructions = dis.get_instructions(self.task)
        instructions = list(instructions)
        # print(self.code_for_ic)
        ic = self.get_ic(instructions)
        # print(dis.findlabels(self.task.__code__.co_code))
        print("Instruction count = ", ic)
        self.instruction_count = ic
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
