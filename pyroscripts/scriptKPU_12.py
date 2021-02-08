import pandas as pd
import numpy as np
import Pyro4
import time
import pymssql
import variable as v
import sys
import json

def KPU_RT_func():   # 12. 실시간 시장

    global RT_Pnet, KPU_RT_dis
    KPU_RT = Pyro4.core.Proxy('PYRO:KPU_RT@220.149.218.226:10100')
    KPU_RT.calculate(v.P2P)
    KPU_RT_dis = KPU_RT.display()
    RT_Pnet = KPU_RT.to_postech()

    data = {}
    data['KPU_12'] = RT_Pnet

    with open('./variable.json','w') as json_file:
        json.dump(data, json_file)
    print(RT_Pnet)

if __name__=="__main__":
    KPU_RT_func()