import pandas as pd
import numpy as np
import Pyro4
import time
import pymssql
import variable as v
import sys
import json

def KPU_SF_func():   # 10. SMP 예측

    KPU_SF = Pyro4.core.Proxy("PYRO:KPU_SF@220.149.218.226:10100")
    with open('./variable.json','r') as json_file:
        json_data = json.load(json_file)
        temp = json_data['POSTECH_6']
        
    smp = KPU_SF.forecast(temp)
    
    data = {}
    data['KPU_10'] = smp

    with open('./variable.json','w') as json_file:
        json.dump(data, json_file)
    print(smp)

if __name__=="__main__":
    KPU_SF_func()