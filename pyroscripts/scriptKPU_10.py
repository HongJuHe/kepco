
import Pyro4
import time
import variable as v
import sys
import json

def KPU_SF_func():   # 10. SMP 예측

    data = {}
    
    KPU_SF = Pyro4.core.Proxy("PYRO:KPU_SF@220.149.218.226:10100")
    with open('./variable.json','r') as json_file:
        json_data = json.load(json_file)
        data.update(json_data)
        temp = json_data['POSTECH_6']
        
    smp = KPU_SF.forecast(temp)
    
    
    
    data['KPU_10'] = smp

    with open('./variable.json','w') as json_file:
        json.dump(data, json_file)
    print(smp)

if __name__=="__main__":
    KPU_SF_func()
    