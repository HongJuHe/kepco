import pandas as pd
import numpy as np
import Pyro4
import time
import pymssql
import variable as v
import sys
import json

def POS_SE_func():   # 8. 상태 추정

    global vm_act, va_act, vm_est, va_est
    POSTECH_server = Pyro4.Proxy("PYRO:POSTECHserver@141.223.165.62:10200")
    with open('./variable.json','r') as json_file:
        json_data = json.load(json_file)
        temp = json_data['KPU_12']
    
    vm_act, va_act, vm_est, va_est = POSTECH_server.POSTECH_SE(temp)

    data = {}
    data['POSTECH_8_1'] = vm_act
    data['POSTECH_8_2'] = va_act
    data['POSTECH_8_3'] = vm_est
    data['POSTECH_8_4'] = va_est

    with open('./variable.json','w') as json_file:
        json.dump(data, json_file)
    print(vm_act)

if __name__=="__main__":
    POS_SE_func()