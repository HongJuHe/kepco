import pandas as pd
import numpy as np
import Pyro4
import time
import pymssql
import sys
import json
import variable as v
global temp

def POS_PV_func():   # 6. PV 발전량 예측

    #global v.pred_PV_pos, v.Zone_gen, v.Zone_load, data_dict, v.pred_PV
    POSTECH_server = Pyro4.Proxy("PYRO:POSTECHserver@141.223.165.62:10200")
    v.pred_PV_pos, v.Zone_gen, v.Zone_load, v.data_dict = POSTECH_server.POSTECH_PV_forecast('20200507')    # 예측하고자 하는 날짜(20년 2월~6월) 삼천포
    v.pred_PV = v.pred_PV_pos
    print(v.pred_PV)


def KPU_SF_func():   # 10. SMP 예측

    #global smp
    v.KPU_SF = Pyro4.core.Proxy("PYRO:KPU_SF@220.149.218.226:10100")
    v.smp = v.KPU_SF.forecast(temp)
    print(v.smp)


def KPU_DA_func():   # 11. 전일 시장

    #global KPU_DA_dis, DA_DLMP, DA_Pnet, Pnet
    KPU_DA = Pyro4.core.Proxy("PYRO:KPU_DA@220.149.218.226:10100")
    KPU_DA.calculate(temp)
    KPU_DA_dis = KPU_DA.display()
    v.DA_DLMP = KPU_DA_dis['DLMP']
    DA_Pnet = KPU_DA.to_postech()
    v.Pnet = DA_Pnet
    print("hi")


def KPU_RT_func():   # 12. 실시간 시장

    #global RT_Pnet, KPU_RT_dis, Pnet
    KPU_RT = Pyro4.core.Proxy('PYRO:KPU_RT@220.149.218.226:10100')
    KPU_RT.calculate(temp)
    v.KPU_RT_dis = KPU_RT.display()
    v.RT_Pnet = KPU_RT.to_postech()
    print(v.RT_Pnet)


def POS_SE_func():   # 8. 상태 추정

    #global vm_act, va_act, vm_est, va_est
    POSTECH_server = Pyro4.Proxy("PYRO:POSTECHserver@141.223.165.62:10200")
    v.vm_act, v.va_act, v.vm_est, v.va_est = POSTECH_server.POSTECH_SE(temp)
    print("상태 추정 중입니다...")


def Scenario_1():

    # 6 -> 10 -> 11 -> 12 -> 8
    POS_PV_func()   #  6. PV 발전량 예측. 입력인자 : '20200507'(특정날짜),   출력인자 : pred_PV
    KPU_SF_func()   #  10. SMP 예측.    입력인자 : pred_PV,            출력인자 : smp
    KPU_DA_func()   #  11. 전일시장.     입력인자 : smp,                 출력인자 : KPU_DA_dis, DA_DLMP
    KPU_RT_func()   #  12. 실시간시장.    입력인자 : P2P,                 출력인자 : RT_Pnet
    POS_SE_func()   #  8. 상태추정.      입력인자 : RT_Pnet,             출력인자 : vm_act, va_act, vm_est, va_est

if __name__=="__main__":

    if sys.argv[1]=='POSTECH_6':
        POS_PV_func()

    elif sys.argv[1]=='KPU_10':
        temp = eval(sys.argv[2])
        KPU_SF_func()

    elif sys.argv[1]=='KPU_11':
        temp = eval(sys.argv[2])
        KPU_DA_func() 

    elif sys.argv[1]=='KPU_12':
        temp = eval(sys.argv[2])
        KPU_RT_func()

    elif sys.argv[1]=='POSTECH_8':
        temp = eval(sys.argv[2])
        POS_SE_func()
    