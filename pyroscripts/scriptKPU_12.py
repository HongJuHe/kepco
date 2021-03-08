
import Pyro4
import time
import variable as v
import sys
import json
import pandas as pd
import numpy as np


def KPU_RT_func():   # 12. 실시간 시장

    data = {}
    time96 = list(range(0,96))
    KPU_RT = Pyro4.core.Proxy('PYRO:KPU_RT@220.149.218.226:10100')
    KPU_RT.calculate(v.P2P)
    KPU_RT_dis = KPU_RT.display()
    RT_Pnet = KPU_RT.to_postech()


    with open('./variable.json','r') as json_file:
        json_data = json.load(json_file)
        data.update(json_data)

        
    data['KPU_12'] = RT_Pnet

    with open('./variable.json','w') as json_file:
        json.dump(data, json_file)
    
    
    # start of the to_csv function #
    KPU_RT_dis = KPU_RT.display()

    RT_DLMP = pd.DataFrame(KPU_RT_dis['DLMP'])
    RT_DLMP = RT_DLMP[['TIME', 'Zone1', 'Zone2', 'Zone3', 'Zone4', 'Zone5']]

    RT_DEMAND = pd.DataFrame(KPU_RT_dis['DEMAND'])
    RT_DEMAND = RT_DEMAND[['Feeder','Agent3','Agent4','Agent5','Agent6','Agent7','Agent8','Agent9','Agent12','Agent13']]
    RT_DEMAND.columns = ['Feeder','Agent-1','Agent-2','Agent-3','Agent-4','Agent-5','Agent-6','Agent-7','Agent-8','Agent-9']
    RT_DEMAND['Feeder'] = np.array(RT_DEMAND['Feeder']*1000)

    for i in range(1,10):
        RT_DEMAND['Agent-{}'.format(i)] =np.array(RT_DEMAND['Agent-{}'.format(i)]*1000)

    RT_DEMAND.insert(0,'Time',time96,True)


    RT_PV_CURTAILMENT = pd.DataFrame(KPU_RT_dis['PV_CURTAILMENT'])
    RT_PV_CURTAILMENT = RT_PV_CURTAILMENT[['TIME', 'PV7', 'PV4', 'PV9', 'PV6', 'PV13', 'SUM']]
    RT_PV_CURTAILMENT.columns = ['Time','Zone-1','Zone-2','Zone-3','Zone-4','Zone-5','Sum']
    RT_PV_CURTAILMENT['Sum'] = np.array(RT_PV_CURTAILMENT['Sum']*1000)

    for i in range(1,6):
        RT_PV_CURTAILMENT['Zone-{}'.format(i)] =np.array(RT_PV_CURTAILMENT['Zone-{}'.format(i)]*1000)


    RT_POWER_FLOW = pd.DataFrame(KPU_RT_dis['POWER_FLOW'])
    RT_POWER_FLOW = RT_POWER_FLOW[['TIME', 'MTR->Zone1', 'Zone1->Zone2', 'Zone1->Zone3', 'Zone1->Zone4', 'Zone1->Zone5']]
    RT_POWER_FLOW['MTR->Zone1'] = np.array(RT_POWER_FLOW['MTR->Zone1']*1000)
    RT_POWER_FLOW['Zone1->Zone2'] = np.array(RT_POWER_FLOW['Zone1->Zone2']*1000)
    RT_POWER_FLOW['Zone1->Zone3'] = np.array(RT_POWER_FLOW['Zone1->Zone3']*1000)
    RT_POWER_FLOW['Zone1->Zone4'] = np.array(RT_POWER_FLOW['Zone1->Zone4']*1000)
    RT_POWER_FLOW['Zone1->Zone5'] = np.array(RT_POWER_FLOW['Zone1->Zone5']*1000)
    RT_POWER_FLOW.columns = ['Time','Bus1 -> Bus2','Bus2 -> Bus3','Bus7 -> Bus8','Bus2 -> Bus5','Bus7 -> Bus12']

    RT_DLMP.to_csv('public/csv/RT_DLMP.csv', index=False)
    RT_DEMAND.to_csv('public/csv/RT_power.csv', index=False)
    RT_PV_CURTAILMENT.to_csv('public/csv/RT_PV_curtailment.csv', index=False)
    RT_POWER_FLOW.to_csv('public/csv/RT_current.csv', index=False)
    # end of the to_csv function #



    


if __name__=="__main__":
    KPU_RT_func()
    print("Success!")
    sys.exit()
