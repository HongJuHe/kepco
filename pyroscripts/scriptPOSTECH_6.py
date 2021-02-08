import pandas as pd
import numpy as np
import Pyro4
import time
import pymssql
import variable as v
import sys
import json

def POS_PV_func():   # 6. PV 발전량 예측

    #global pred_PV_pos, Zone_gen, Zone_load, data_dict, pred_PV
    POSTECH_server = Pyro4.Proxy("PYRO:POSTECHserver@141.223.165.62:10200")
    v.pred_PV_pos, v.Zone_gen, v.Zone_load, v.data_dict = POSTECH_server.POSTECH_PV_forecast('20200507')    # 예측하고자 하는 날짜(20년 2월~6월) 삼천포
    pred_PV = v.pred_PV_pos

    data = {}
    data['POSTECH_6'] = pred_PV

    with open('./variable.json','w') as json_file:
        json.dump(data, json_file)
    print(pred_PV)



if __name__=="__main__":
    POS_PV_func()