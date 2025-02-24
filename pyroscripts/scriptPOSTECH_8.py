import Pyro4
import time
import variable as v
import sys
import json
import pandas as pd
import numpy as np



def POS_SE_func():   # 8. 상태 추정


    data = {}
    time96 = list(range(0,96))
    global vm_act, va_act, vm_est, va_est
    POSTECH_server = Pyro4.Proxy("PYRO:POSTECHserver@141.223.165.62:10200")

    with open('./variable.json','r') as json_file:
        json_data = json.load(json_file)
        data.update(json_data)
        temp = json_data['KPU_12']

    vm_act, va_act, vm_est, va_est = POSTECH_server.POSTECH_SE(temp)

        
    data['POSTECH_8_1'] = vm_act
    data['POSTECH_8_2'] = va_act
    data['POSTECH_8_3'] = vm_est
    data['POSTECH_8_4'] = va_est

    with open('./variable.json','w') as json_file:
        json.dump(data, json_file)
    

    # start of the to_csv function #
    vm_est = pd.DataFrame(vm_est, columns=['Node-{}'.format(i) for i in range(1,14)])   # estimated voltage magnitude (p.u.)
    vm_est.insert(0,'Time',time96,True)
    va_est = pd.DataFrame(va_est, columns=['Node-{}'.format(i) for i in range(1,14)])   # estimated voltage angle (radian)
    va_est.insert(0,'Time',time96,True)
    vm_est.to_csv('public/csv/actual_mag.csv', index=False)
    va_est.to_csv('public/csv/actual_ang.csv', index=False)
    
    # end of the to_csv function #

    print("Success!")
    quit()

    

if __name__=="__main__":
    POS_SE_func()
    