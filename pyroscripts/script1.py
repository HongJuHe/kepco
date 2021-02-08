import pandas as pd
import numpy as np
import Pyro4
import time
import pymssql
import sys
global temp

# start of the global Variable #

pred_PV = 0   # 10. SMP 모듈 입력인자
Pnet = 0

# end of the global Variable #


# start of the KPU Variables #

smp = 0        # 24x1      Price

KPU_DA_dis = 0  # 24x20
DA_Pnet = 0     # 24x13.    Time(24h), node2(kW), node3(kW), ... , node12(kW), node13(kW)
DA_DLMP = 0     # 24x6.     Time(24h), Zone2, Zone3, Zone4, Zone5  --> 3번 입력인자

RT_Pnet = 0     # 96x13.    Time(15m), node2(kW), node3(kW), ... , node12(kW), node13(kW)  --> 8번 입력인자
KPU_RT_dis = 0

# end of the KPU Variables #


# start of the INHA Variables #

pred_PV_inha = 0    # 24x2.     Time, Renew(kW)
data_dict ={'pv_data':{'TIME':[],'Zone-1 generation':[], 'Zone-2 generation':[], 'Zone-3 generation':[], 'Zone-4 generation':[], 'Zone-5 generation':[]},
          'load_data':{'TIME':[],'Zone-1 load':[], 'Zone-2 load':[], 'Zone-3 load':[], 'Zone-4 load':[], 'Zone-5 load':[]}}  # 3번 입력인자

P2P = 0     # 12번 입력인자

p2p_trade = 0       # 480x5.    Time, Provide, Consumer, Amount, Price
p2p_amount = 0      # 480x1.    Amount  --> 9번 입력인자

# end of the INHA Variables #


# start of the POSTECH Variables #

pred_PV_pos = 0     # 24x2.     Time(24h), Renew(kW)
Zone_gen = 0        # 24x6      Time(24h), Zone-1 gen(kW), Zone-2 gen(kW), Zone-3 gen(kW), Zone-4 gen(kW), Zone-5 gen(kW)      ┐
Zone_load = 0       # 24x6      Time(24h), Zone-1 load(kW), Zone-2 load(kW), Zone-3 load(kW), Zone-4 load(kW), Zone-5 load(kW) ┘ 3번 입력인자 data_dict 생성용 변수

Pgen = 0        # 24x13.    Time(24h), node2(kW), node3(kW), ... , node12(kW), node13(kW)
ED_Pnet = 0     # 24x13.    Time(24h), node2(kW), node3(kW), ... , node12(kW), node13(kW)
Pload = 0       # 24x13.    Time(24h), node2(kW), node3(kW), ... , node12(kW), node13(kW)

vm_act = 0      # 96x13.    node1(PU), node2(PU), node3(PU), ... , node12(PU), node13(PU)
va_act = 0      # 96x13.    node1(deg), node2(deg), node3(deg), ... , node12(deg), node13(deg)
vm_est = 0      # 96x13.    node1(PU), node2(PU), node3(PU), ... , node12(PU), node13(PU)
va_est = 0      # 96x13.    node1(deg), node2(deg), node3(deg), ... , node12(deg), node13(deg)

trade_energy = 0    # 24x20.    Amount
trade_encode = 0    # 27x20.    ???
trade_decode = 0    # 24x20.    ???

# end of the POSTECH Variables #


def POS_PV_func():   # 6. PV 발전량 예측

    global pred_PV_pos, Zone_gen, Zone_load, data_dict, pred_PV
    POSTECH_server = Pyro4.Proxy("PYRO:POSTECHserver@141.223.165.62:10200")
    pred_PV_pos, Zone_gen, Zone_load, data_dict = POSTECH_server.POSTECH_PV_forecast('20200507')    # 예측하고자 하는 날짜(20년 2월~6월) 삼천포
    pred_PV = pred_PV_pos
    print(pred_PV)


def KPU_SF_func():   # 10. SMP 예측

    global smp
    KPU_SF = Pyro4.core.Proxy("PYRO:KPU_SF@220.149.218.226:10100")
    smp = KPU_SF.forecast(temp)
    print(smp)

def KPU_DA_func():   # 11. 전일 시장

    global KPU_DA_dis, DA_DLMP, DA_Pnet, Pnet
    KPU_DA = Pyro4.core.Proxy("PYRO:KPU_DA@220.149.218.226:10100")
    KPU_DA.calculate(temp)
    KPU_DA_dis = KPU_DA.display()
    DA_DLMP = KPU_DA_dis['DLMP']
    DA_Pnet = KPU_DA.to_postech()
    Pnet = DA_Pnet
    print(Pnet)


def KPU_RT_func():   # 12. 실시간 시장

    global RT_Pnet, KPU_RT_dis, Pnet
    KPU_RT = Pyro4.core.Proxy('PYRO:KPU_RT@220.149.218.226:10100')
    KPU_RT.calculate(P2P)
    KPU_RT_dis = KPU_RT.display()
    RT_Pnet = KPU_RT.to_postech()
    print("sc")


def POS_SE_func():   # 8. 상태 추정

    global vm_act, va_act, vm_est, va_est
    POSTECH_server = Pyro4.Proxy("PYRO:POSTECHserver@141.223.165.62:10200")
    vm_act, va_act, vm_est, va_est = POSTECH_server.POSTECH_SE(RT_Pnet)


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

    elif sys.argv[1]==''




