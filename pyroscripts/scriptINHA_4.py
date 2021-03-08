import json
import Pyro4
import pandas as pd
import numpy as np
import time
import pymssql

zone_requests = 0
P2P_hourly_data = None


def INHA_P2PMatching_func():   # 4. P2P 매칭

    global DA_DLMP, zone_requests, p2p_trade, p2p_amount, P2P, P2P_hourly_data
    
    data_dict ={'pv_data':{'TIME':[],'Zone-1 generation':[], 'Zone-2 generation':[], 'Zone-3 generation':[], 'Zone-4 generation':[], 'Zone-5 generation':[]},
          'load_data':{'TIME':[],'Zone-1 load':[], 'Zone-2 load':[], 'Zone-3 load':[], 'Zone-4 load':[], 'Zone-5 load':[]}} 

    DA_DLMP = {}

    bid_requests = Pyro4.core.Proxy('PYRO:INHA_BID@165.246.42.65:10010')
    inham5_lmk_module = Pyro4.core.Proxy('PYRO:exam@165.246.44.252:10001')

    bid_requests.load(data_dict, DA_DLMP)

    for time in range(24):

        zone_requests = bid_requests.requests(P2P_hourly_data, time) # 모듈 실제 동작
        P2P_hourly_data = inham5_lmk_module.receive_hourly_data(zone_requests, time)


    p2p_trade = inham5_lmk_module.get_results()
    p2p_amount = p2p_trade['Result']['Amount']
    Result = pd.DataFrame(p2p_trade['Result'])
    Result.to_csv('public/csv/inha_transaction.csv', index=False)
    # end of the to_csv function #

if __name__=="__main__":
    
    INHA_P2PMatching_func()
    print("Success!")