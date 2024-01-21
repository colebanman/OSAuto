import random
import string
import time

class Task():

    taskId = None
    taskType = None

    def __init__(self, taskType):
        # generate taskId
        self.taskId = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3)) + '-' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3)) + '-' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
        self.taskType = taskType
    
    def setStatus(self, text, color):
        # print in format [TIME] | [TASKID] | [TEXT]
        if color == "good":
            print(f"\033[92m[{time.strftime('%H:%M:%S')}] | [{self.taskId}] | {text}\033[0m")
        elif color == "bad":
            print(f"\033[91m[{time.strftime('%H:%M:%S')}] | [{self.taskId}] | {text}\033[0m")
        elif color == "warning":
            print(f"\033[93m[{time.strftime('%H:%M:%S')}] | [{self.taskId}] | {text}\033[0m")
        else:
            print(f"\033[94m[{time.strftime('%H:%M:%S')}] | [{self.taskId}] | {text}\033[0m")