from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import random
from base64 import b64encode, b64decode
import pstats
import time


class ObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return super().default(obj)
        try:
            encoded = {'_python_object': b64encode(pickle.dumps(obj)).decode('utf-8')}
            return encoded
        except:
            print("Error while encoding the object")
            exit()


def as_python_object(dct):
    if '_python_object' in dct:
        try:
            decoded = pickle.loads(b64decode(dct['_python_object'].encode('utf-8')))
            return decoded
        except:
            print("Error while decoding the object")
            exit()
    return dct













def get_estimated_time(task):
    start_time = time.time()
    time.sleep(0.0001)
    task()
    end_time = time.time()
    time_taken = (end_time - start_time) - 0.0001
    return time_taken

def get_instruction_count(task):
    pass
