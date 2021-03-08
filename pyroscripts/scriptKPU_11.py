import Pyro4
import time
import variable as v
import sys
import json
import pandas as pd
import numpy as np



def KPU_DA_func():   # 11. 전일 시장

    KPU_DA = Pyro4.core.Proxy("PYRO:KPU_DA@220.149.218.226:10100")

    data = {}
    time24 = list(range(0,24))

    with open('./variable.json','r') as json_file:
        json_data = json.load(json_file)
        data.update(json_data)
        temp = json_data['KPU_10']

    KPU_DA.calculate(temp)
    KPU_DA_dis = KPU_DA.display()
    DA_DLMP = KPU_DA_dis['DLMP']
    DA_Pnet = KPU_DA.to_postech()
    Pnet = DA_Pnet

    data['KPU_11_1'] = KPU_DA_dis
    data['KPU_11_2'] = DA_DLMP

    resultString = DA_DLMP

    v.Pnet = DA_Pnet

    with open('./variable.json','w') as json_file:
        json.dump(data, json_file)



    # start of the to_csv function #
    KPU_DA_dis = KPU_DA.display()
    
    DA_DLMP = pd.DataFrame(KPU_DA_dis['DLMP'])
    DA_DLMP = DA_DLMP[['TIME', 'Zone1', 'Zone2', 'Zone3', 'Zone4', 'Zone5']]


    DA_DEMAND = pd.DataFrame(KPU_DA_dis['DEMAND'])
    DA_DEMAND = DA_DEMAND[['Feeder','Agent3','Agent4','Agent5','Agent6','Agent7','Agent8','Agent9','Agent12','Agent13']]
    DA_DEMAND.columns = ['Feeder','Agent-1','Agent-2','Agent-3','Agent-4','Agent-5','Agent-6','Agent-7','Agent-8','Agent-9']
    DA_DEMAND['Feeder'] = np.array(DA_DEMAND['Feeder']*1000)

    for i in range(1,10):
        DA_DEMAND['Agent-{}'.format(i)] =np.array(DA_DEMAND['Agent-{}'.format(i)]*1000)

    DA_DEMAND.insert(0,'Time',time24,True)

    DA_PV_CURTAILMENT = pd.DataFrame(KPU_DA_dis['PV_CURTAILMENT'])
    DA_PV_CURTAILMENT = DA_PV_CURTAILMENT[['TIME', 'PV7', 'PV4', 'PV9', 'PV6', 'PV13', 'SUM']]
    DA_PV_CURTAILMENT.columns = ['Time','Zone-1','Zone-2','Zone-3','Zone-4','Zone-5','Sum']
    DA_PV_CURTAILMENT['Sum'] = np.array(DA_PV_CURTAILMENT['Sum']*1000)

    for i in range(1,6):
        DA_PV_CURTAILMENT['Zone-{}'.format(i)] =np.array(DA_PV_CURTAILMENT['Zone-{}'.format(i)]*1000)

    DA_POWER_FLOW = pd.DataFrame(KPU_DA_dis['POWER_FLOW'])
    DA_POWER_FLOW = DA_POWER_FLOW[['TIME', 'MTR->Zone1', 'Zone1->Zone2', 'Zone1->Zone3', 'Zone1->Zone4', 'Zone1->Zone5']]
    DA_POWER_FLOW['MTR->Zone1'] = np.array(DA_POWER_FLOW['MTR->Zone1']*1000)
    DA_POWER_FLOW['Zone1->Zone2'] = np.array(DA_POWER_FLOW['Zone1->Zone2']*1000)
    DA_POWER_FLOW['Zone1->Zone3'] = np.array(DA_POWER_FLOW['Zone1->Zone3']*1000)
    DA_POWER_FLOW['Zone1->Zone4'] = np.array(DA_POWER_FLOW['Zone1->Zone4']*1000)
    DA_POWER_FLOW['Zone1->Zone5'] = np.array(DA_POWER_FLOW['Zone1->Zone5']*1000)
    DA_POWER_FLOW.columns = ['Time','Bus1 -> Bus2','Bus2 -> Bus3','Bus7 -> Bus8','Bus2 -> Bus5','Bus7 -> Bus12']

    DA_DLMP.to_csv('public/csv/DA_DLMP.csv', index=False)
    DA_DEMAND.to_csv('public/csv/DA_power.csv', index=False)
    DA_PV_CURTAILMENT.to_csv('public/csv/DA_PV_curtailment.csv', index=False)
    DA_POWER_FLOW.to_csv('public/csv/DA_current.csv', index=False)




    # end of the to_csv function #

    print(resultString)
    sys.exit()

    
    

if __name__=="__main__":
    KPU_DA_func()