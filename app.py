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
N = 12622*10**4 #日本の総人口(2020年時点)
I = 10000
R = 0
D = 0
S = N - I - R - D 
t = 0

# 各パラメータの設定
contact_num = 14 #流行前の平均接触人数(１日における一人当たり)
emergency_contact_num = contact_num * 0.2 #緊急事態宣言時は、平時の2割程度の接触回数
infetion_rate = 0.01
healing_rate = 0.01
loop_num = 500
emergency_loop_num = 30
emergency_start = 80
emergency_stop = emergency_start + emergency_loop_num
delta_t = 1
exposed_num = 5
death_rate = 0.001
death_num = 20

CN = contact_num
ECN = emergency_contact_num
IR = infetion_rate
HR = healing_rate
DR = death_rate

"""
# 結果記録用のリスト
t_list = []
S_list = []
I_list = []
R_list = []
D_list = []
"""

def  loop_process(S, I, R, D, N, loop_num, emergency_start, emergency_stop, delta_t) :
  
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

    return t_list, S_list, I_list, R_list, D_list  
    
t_list, S_list, I_list, R_list, D_list = loop_process(S, I, R, D, N, loop_num, emergency_start, emergency_stop, delta_t)    
    

fig = plt.figure(figsize=(10, 6))
plt.plot(t_list, S_list, label='S', linewidth=2)
plt.plot(t_list, I_list, label='I', linewidth=2)
plt.plot(t_list, R_list, label='R', linewidth=2)
plt.plot(t_list, D_list, label='D', linewidth=2)

plt.title('Population Rate-Time')
plt.xlabel('Time')
plt.ylabel('Population Rate')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
# 緊急事態宣言期間を示す縦線
plt.axvline(x=emergency_start, color='red', linestyle='--', alpha=0.7, label='emergency_start')
plt.axvline(x=emergency_stop, color='red', linestyle='--', alpha=0.7, label='emergency_stop')

plt.show()
fig.savefig('InfectionSimulation.png', dpi=300, bbox_inches='tight')

"""
2020年緊急事態宣言(4月-5月の一か月間)
感染した人は7日間の経済活動停止と仮定する
死者は死亡してから先はずっと経済活動ができないとする
日本全体の経済活動の結果の合計金額をsum_financeとおいて計算する
sum_economic_loss = 全体の経済損失
緊急事態宣言を行うとき、一日あたり3339億円の経済的損失が発生すると仮定
2020年4-6月の実質GDPから、国民一人の、一日あたりの実質GDP=10783円
"""
emergency_economic_loss = 3339*10**8 * emergency_loop_num
infected_economic_loss = 10783*I_list[-1]*7 #7は活動停止期間(日)
sum_economic_loss = emergency_economic_loss + infected_economic_loss

print(f"緊急事態宣言による経済損失: {emergency_economic_loss:.2e}円")
print(f"感染による経済損失: {infected_economic_loss:.2e}円")
print(f"総合的な経済損失: {sum_economic_loss:.2e}円")
