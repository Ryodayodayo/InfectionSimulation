import matplotlib.pyplot as plt
import tqdm

"""
S→健康な人
I→感染者
R→免疫獲得者
D→死亡した人
infetion_rate→感染率
healing_rate→治癒率
loop_num→ループする日数
delta_t→差分(時間)
death_rate→死亡率
death_num→死亡するまでの日数

微分計算はべき級数展開の一次までの近似を用いる
"""

# 初期条件
S = 0.99
I = 0.01
R = 0
D = 0
t = 0

# 各パラメータの設定
infetion_rate = 1.7
healing_rate = 0.8
loop_num = 3000
delta_t = 0.01
exposed_num = 5
death_rate = 0.03
death_num = 20

IR = infetion_rate
HR = healing_rate
LN = loop_num
DR = death_rate
DN = death_num

# 結果記録用のリスト
t_list = []
S_list = []
I_list = []
R_list = []

for t in range(loop_num):
    new_S = S + delta_t * (-IR * S * I)
    new_I = I + delta_t * (IR* S * I - HR * I)
    new_R = R + delta_t * (HR * I)
    new_D = D + delta_t * DR * (1/DN) * I

    t_list.append(t)
    S_list.append(new_S)
    I_list.append(new_I)
    R_list.append(new_R)
    S = new_S
    I = new_I
    R = new_R

    t = t + delta_t 

fig = plt.figure()
plt.plot(t_list, S_list, label='S')
plt.plot(t_list, I_list, label='I')
plt.plot(t_list, R_list, label='R')

plt.title('Population Rate-Time')
plt.xlabel('Time')
plt.ylabel('Population Rate')
plt.legend()
plt.show()
fig.savefig('./SIR_P-T.png')

print('\n --DONE-- \n')
