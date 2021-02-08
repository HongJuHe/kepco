import pandas as pd
import numpy as np
import Pyro4
import time
import pymssql
import variable as v
import sys
import json

def KPU_DA_func():   # 11. 전일 시장

    #global KPU_DA_dis, DA_DLMP, DA_Pnet, Pnet
    KPU_DA = Pyro4.core.Proxy("PYRO:KPU_DA@220.149.218.226:10100")
    with open('./variable.json','r') as json_file:
        json_data = json.load(json_file)
        temp = json_data['KPU_10']

    KPU_DA.calculate(temp)
    KPU_DA_dis = KPU_DA.display()
    DA_DLMP = KPU_DA_dis['DLMP']
    DA_Pnet = KPU_DA.to_postech()

    data = {}
    data['KPU_11_1'] = KPU_DA_dis
    data['KPU_11_2'] = DA_DLMP
    v.Pnet = DA_Pnet

    with open('./variable.json','w') as json_file:
        json.dump(data, json_file)
    print(KPU_DA_dis)

if __name__=="__main__":
    KPU_DA_func()