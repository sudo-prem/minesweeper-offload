from xmlrpc.server import SimpleXMLRPCServer
from json import loads, JSONEncoder, dumps
import random
import pickle
from base64 import b64decode, b64encode
from device_profiler import *
from code_sync import CodeSync
from minesweeper import Sentence, MinesweeperAI
from object_encoder import ObjectEncoder, as_python_object

# Functions to register
local_frequency = DeviceProfiler().get_local_cpu_frequency
local_CPI = DeviceProfiler().get_local_CPI


def safe_move_remote(code_sync):
    code_sync_remote = loads(code_sync, object_hook=as_python_object)

    # print(code_sync_remote.mines, code_sync_remote.safes, code_sync_remote.knowledge, code_sync_remote.sentenceList)
    msAI = MinesweeperAI()
    msAI.safes = code_sync_remote.safes
    msAI.mines = code_sync_remote.mines
    msAI.knowledge = code_sync_remote.knowledge
    msAI.sentenceList = code_sync_remote.sentenceList
    msAI.conclusion()

    code_sync_Return = CodeSync(msAI.sentenceList, msAI.knowledge,
                                msAI.mines, msAI.safes)
    res = dumps(code_sync_Return, cls=ObjectEncoder)
    return res


if __name__ == '__main__':
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000...")
    server.register_function(local_frequency, "local_frequency")
    server.register_function(local_CPI, "local_CPI")
    server.register_function(safe_move_remote, "safe_move_remote")
    server.serve_forever()
