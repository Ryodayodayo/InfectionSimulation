import matplotlib.pyplot as plt
import logging

"""
N→総人口
S→健康な人
I→感染者
R→免疫獲得者
D→死亡した人

contact_num→一日の一人当たりの接触人数
infetion_rate→感染率
healing_rate→治癒率
loop_num→ループする日数
delta_t→差分(時間)
death_rate→死亡率
death_num→死亡するまでの日数

微分計算はべき級数展開の一次までの近似を用いる
"""

# 初期条件
S = 100000
I = 5
R = 0
D = 0
N = S + I + R
t = 0

# 各パラメータの設定
contact_num = 14 #流行前の平均接触人数(１日における一人当たり)
emergency_contact_num = contact_num * 0.2 #緊急事態宣言時は、平時の2割程度の接触率
infetion_rate = 0.01
healing_rate = 0.03
loop_num = 300
emergency_loop_num = 100
emergency_start = 50
emergency_stop = emergency_start + emergency_loop_num
delta_t = 1
exposed_num = 5
death_rate = 0.03
death_num = 20

CN = contact_num
ECN = emergency_contact_num
IR = infetion_rate
HR = healing_rate
DR = death_rate

# 結果記録用のリスト
t_list = []
S_list = []
I_list = []
R_list = []
D_list = []

for t in range(loop_num):
    if emergency_start <= t <=emergency_stop : 

        new_S = S + delta_t * (-IR * ECN * (I/N) * S) #I/N→人口における感染してる人の割合、
        new_I = I + delta_t * (IR * ECN * (I/N) * S - HR * I)
        new_R = R + delta_t * ((1-DR)*HR * I)
        new_D = D + delta_t * (DR * HR * I)

        """すべての微分形の足し算→0""" #(-IR * CN * (I/N) * S)+(IR * CN * (I/N) * S - HR * I)+((1-DR)*HR * I)+(DR * HR * I)

        t_list.append(t)
        S_list.append(new_S)
        I_list.append(new_I)
        R_list.append(new_R)
        D_list.append(new_D)

        S = new_S
        I = new_I
        R = new_R
        D = new_D

        t = t + delta_t 


    else : 
        new_S = S + delta_t * (-IR * CN * (I/N) * S) #I/N→人口における感染してる人の割合、
        new_I = I + delta_t * (IR * CN * (I/N) * S - HR * I)
        new_R = R + delta_t * ((1-DR)*HR * I)
        new_D = D + delta_t * (DR * HR * I)

        """すべての微分形の足し算→0""" #(-IR * CN * (I/N) * S)+(IR * CN * (I/N) * S - HR * I)+((1-DR)*HR * I)+(DR * HR * I)

        t_list.append(t)
        S_list.append(new_S)
        I_list.append(new_I)
        R_list.append(new_R)
        D_list.append(new_D)

        S = new_S
        I = new_I
        R = new_R
        D = new_D

        t = t + delta_t 
    

fig = plt.figure()
plt.plot(t_list, S_list, label='S')
plt.plot(t_list, I_list, label='I')
plt.plot(t_list, R_list, label='R')
plt.plot(t_list, D_list, label='D')

plt.title('Population Rate-Time')
plt.xlabel('Time')
plt.ylabel('Population Rate')
plt.legend()
plt.show()
fig.savefig('InfectionSimulation.png')

"""2020年緊急事態宣言(4月-5月の一か月間)"""
