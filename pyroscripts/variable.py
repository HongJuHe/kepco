# start of the global Variable #

pred_PV = 0   # 10. SMP 모듈 입력인자
Pnet = 0

# end of the global Variable #


# start of the KPU Variables #

smp = 0         # 24x1      Price

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

pred_PV_pos = 0    # 24x2.     Time(24h), Renew(kW)
Zone_gen = 0       # 24x6      Time(24h), Zone-1 gen(kW), Zone-2 gen(kW), Zone-3 gen(kW), Zone-4 gen(kW), Zone-5 gen(kW)      ┐
Zone_load = 0      # 24x6      Time(24h), Zone-1 load(kW), Zone-2 load(kW), Zone-3 load(kW), Zone-4 load(kW), Zone-5 load(kW) ┘ 3번 입력인자 data_dict 생성용 변수

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

def make_Text(name, mylist):
    text = open("./list.txt", "a+")
    text.write(name)
    text.write("\n")
    text.write(mylist)
    text.write("\n")
    text.close()
