import matplotlib.pyplot as plt
import numpy as np


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
I_initial = 10000
R_initial = 0
D_initial = 0
S_initial = N - I_initial - R_initial - D_initial 

# 各パラメータの設定
contact_num = 14 #流行前の平均接触人数(１日における一人当たり)
emergency_contact_num = contact_num * 0.2 #緊急事態宣言時は、平時の2割程度の接触回数
infetion_rate = 0.01 #1接触あたりの感染確率
healing_rate = 0.03
loop_num = 500
emergency_loop_num = 30
emergency_start = 80
emergency_stop = emergency_start + emergency_loop_num
delta_t = 1
exposed_num = 5
death_rate = 0.001
death_num = 20
incubation_period = 3 #潜伏期間


CN = contact_num
ECN = emergency_contact_num
IR = infetion_rate
HR = healing_rate
DR = death_rate

#以下で再生産数Rtを定義してる Rt > 1 で感染が広がる

def loop_process_with_emergency(S, I, R, D, N, loop_num, emergency_start, emergency_stop, delta_t):
    """緊急事態宣言ありのシミュレーション"""
    t_list = []
    S_list = []
    I_list = []
    R_list = []
    D_list = []
    Rt_list = [] #実効再生産数のリスト
    daily_deaths = [] #各日の新規死亡者数を記録

    for t in range(loop_num):
        prev_D = D  # 前日の累計死亡者数
        current_contact_num_val = CN # デフォルトは通常時の接触人数

        if emergency_start <= t <= emergency_stop: 
            # 緊急事態宣言期間中
            current_contact_num_val = ECN # 緊急事態宣言期間中の接触人数
            new_S = S + delta_t * (-IR * ECN * (I/N) * S)
            new_I = I + delta_t * (IR * ECN * (I/N) * S - HR * I)
            new_R = R + delta_t * ((1-DR)*HR * I)
            new_D = D + delta_t * (DR * HR * I)
        else:
            # 通常期間
            new_S = S + delta_t * (-IR * CN * (I/N) * S)
            new_I = I + delta_t * (IR * CN * (I/N) * S - HR * I)
            new_R = R + delta_t * ((1-DR)*HR * I)
            new_D = D + delta_t * (DR * HR * I)

        Rt = (current_contact_num_val * IR * (S / N)) / HR

        # その日の新規死亡者数を計算
        new_deaths = new_D - prev_D
        daily_deaths.append(new_deaths)    

        t_list.append(t)
        S_list.append(new_S)
        I_list.append(new_I)
        R_list.append(new_R)
        D_list.append(new_D)
        Rt_list.append(Rt)


        S = new_S
        I = new_I
        R = new_R
        D = new_D

    return t_list, S_list, I_list, R_list, D_list, Rt_list, daily_deaths

def loop_process_without_emergency(S, I, R, D, N, loop_num, delta_t):
    """緊急事態宣言なしのシミュレーション"""
    t_list = []
    S_list = []
    I_list = []
    R_list = []
    D_list = []
    Rt_list = [] #実効再生産数のリスト
    daily_deaths = []  # 各日の新規死亡者数を記録

    for t in range(loop_num):
        prev_D = D  # 前日の累計死亡者数
        current_contact_num_val = CN # 常に通常の接触回数
        new_S = S + delta_t * (-IR * CN * (I/N) * S)
        new_I = I + delta_t * (IR * CN * (I/N) * S - HR * I)
        new_R = R + delta_t * ((1-DR)*HR * I)
        new_D = D + delta_t * (DR * HR * I)

        Rt = (current_contact_num_val * IR * (S / N)) / HR

        # その日の新規死亡者数を計算
        new_deaths = new_D - prev_D
        daily_deaths.append(new_deaths)

        t_list.append(t)
        S_list.append(new_S)
        I_list.append(new_I)
        R_list.append(new_R)
        D_list.append(new_D)
        Rt_list.append(Rt)

        S = new_S
        I = new_I
        R = new_R
        D = new_D

    return t_list, S_list, I_list, R_list, D_list,Rt_list, daily_deaths

def calculate_death_economic_loss(daily_deaths, total_days):
    """死亡者による経済損失を計算"""
    total_loss = 0
    daily_loss_per_person = 10783  # 一人当たり日額経済損失
    
    for death_day, deaths_count in enumerate(daily_deaths):
        # その日に死亡した人数 × 残り日数 × 日額損失
        remaining_days = total_days - death_day
        loss_from_this_day = deaths_count * remaining_days * daily_loss_per_person
        total_loss += loss_from_this_day
    
    return total_loss


# 緊急事態宣言あり
t_list_with, S_list_with, I_list_with, R_list_with, D_list_with, Rt_list_with, daily_deaths_with = loop_process_with_emergency(
    S_initial, I_initial, R_initial, D_initial, N, loop_num, emergency_start, emergency_stop, delta_t)

# 緊急事態宣言なし
t_list_without, S_list_without, I_list_without, R_list_without, D_list_without, Rt_list_without, daily_deaths_without = loop_process_without_emergency(
    S_initial, I_initial, R_initial, D_initial, N, loop_num, delta_t)

# グラフ作成
fig, axes = plt.subplots(3, 2, figsize=(15, 12))
fig.suptitle('InfectionSimulation', fontsize=16)

# 1. 健康な人
axes[0, 0].plot(t_list_with, S_list_with, label='With Emergency', linewidth=2, color='blue')
axes[0, 0].plot(t_list_without, S_list_without, label='Without Emergency', linewidth=2, color='red')
axes[0, 0].axvline(x=emergency_start, color='gray', linestyle='--', alpha=0.7, label='emergency_start')
axes[0, 0].axvline(x=emergency_stop, color='gray', linestyle='--', alpha=0.7, label='emergency_end')
axes[0, 0].set_title('S')
axes[0, 0].set_xlabel('time (day)')
axes[0, 0].set_ylabel('population')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2. 感染者数の比較
axes[0, 1].plot(t_list_with, I_list_with, label='With Emergency', linewidth=2, color='blue')
axes[0, 1].plot(t_list_without, I_list_without, label='Without Emergency', linewidth=2, color='red')
axes[0, 1].axvline(x=emergency_start, color='gray', linestyle='--', alpha=0.7, label='emergency_start')
axes[0, 1].axvline(x=emergency_stop, color='gray', linestyle='--', alpha=0.7, label='emergency_end')
axes[0, 1].set_title('I')
axes[0, 1].set_xlabel('time (day)')
axes[0, 1].set_ylabel('population')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 3. 回復者数の比較
axes[1, 0].plot(t_list_with, R_list_with, label='With Emergency', linewidth=2, color='blue')
axes[1, 0].plot(t_list_without, R_list_without, label='Without Emergency', linewidth=2, color='red')
axes[1, 0].axvline(x=emergency_start, color='gray', linestyle='--', alpha=0.7, label='emergency_start')
axes[1, 0].axvline(x=emergency_stop, color='gray', linestyle='--', alpha=0.7, label='emergency_end')
axes[1, 0].set_title('R')
axes[1, 0].set_xlabel('time (day)')
axes[1, 0].set_ylabel('population')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# 4. 死亡者数の比較
axes[1, 1].plot(t_list_with, D_list_with, label='With Emergency', linewidth=2, color='blue')
axes[1, 1].plot(t_list_without, D_list_without, label='Without Emergency', linewidth=2, color='red')
axes[1, 1].axvline(x=emergency_start, color='gray', linestyle='--', alpha=0.7, label='emergency_start')
axes[1, 1].axvline(x=emergency_stop, color='gray', linestyle='--', alpha=0.7, label='emergency_end')
axes[1, 1].set_title('D')
axes[1, 1].set_xlabel('time (day)')
axes[1, 1].set_ylabel('population')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# 5. 全体の比較（S, I, R, D）- 緊急事態宣言あり
axes[2, 0].plot(t_list_with, S_list_with, label='S', linewidth=2, color='green')
axes[2, 0].plot(t_list_with, I_list_with, label='I', linewidth=2, color='orange')
axes[2, 0].plot(t_list_with, R_list_with, label='R', linewidth=2, color='blue')
axes[2, 0].plot(t_list_with, D_list_with, label='D', linewidth=2, color='red')
axes[2, 0].axvline(x=emergency_start, color='gray', linestyle='--', alpha=0.7, label='emergency_start')
axes[2, 0].axvline(x=emergency_stop, color='gray', linestyle='--', alpha=0.7, label='emergency_end')
axes[2, 0].set_title('S,I,R,D')
axes[2, 0].set_xlabel('time (day)')
axes[2, 0].set_ylabel('population')
axes[2, 0].legend()
axes[2, 0].grid(True, alpha=0.3)

# 6. 実効再生産数 Rt - 緊急事態宣言あり
axes[2, 1].plot(t_list_with, Rt_list_with, label='Rt', linewidth=2, color='green')
axes[2, 1].axvline(x=emergency_start, color='gray', linestyle='--', alpha=0.7, label='emergency_start')
axes[2, 1].axvline(x=emergency_stop, color='gray', linestyle='--', alpha=0.7, label='emergency_end')
axes[2, 1].set_title('emergency_Rt')
axes[2, 1].set_xlabel('time (day)')
axes[2, 1].set_ylabel('population')
axes[2, 1].legend()
axes[2, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 経済損失計算と比較
print("\n経済損失比較")

# 緊急事態宣言ありの場合
emergency_economic_loss = 3339*10**8 * emergency_loop_num
infected_economic_loss_with = 10783 * I_list_with[-1] * 7
death_economic_loss_with = calculate_death_economic_loss(daily_deaths_with, loop_num)
sum_economic_loss_with = emergency_economic_loss + infected_economic_loss_with + death_economic_loss_with

# 緊急事態宣言なしの場合
infected_economic_loss_without = 10783 * I_list_without[-1] * 7
death_economic_loss_without = calculate_death_economic_loss(daily_deaths_without, loop_num)
sum_economic_loss_without = infected_economic_loss_without + death_economic_loss_without

print(f"\n緊急事態宣言あり")
print(f"緊急事態宣言による経済損失: {emergency_economic_loss:.2e}円")
print(f"感染による経済損失: {infected_economic_loss_with:.2e}円")
print(f"死亡による経済損失: {death_economic_loss_with:.2e}円")
print(f"総合的な経済損失: {sum_economic_loss_with:.2e}円")

print(f"\n緊急事態宣言なし")
print(f"感染による経済損失: {infected_economic_loss_without:.2e}円")
print(f"死亡による経済損失: {death_economic_loss_without:.2e}円")
print(f"総合的な経済損失: {sum_economic_loss_without:.2e}円")

print(f"\n比較結果")
print(f"感染者数の差: {I_list_without[-1] - I_list_with[-1]:.0f}人")
print(f"死亡者数の差: {D_list_without[-1] - D_list_with[-1]:.0f}人")
print(f"死亡による経済損失の差: {death_economic_loss_without - death_economic_loss_with:.2e}円")
print(f"経済損失の差: {sum_economic_loss_with - sum_economic_loss_without:.2e}円")

if sum_economic_loss_with < sum_economic_loss_without:
    print("→ 緊急事態宣言により総経済損失が削減されました")
else:
    print("→ 緊急事態宣言により総経済損失が増加しました")

# グラフを保存
fig.savefig('InfectionSimulation_Comparison.png', dpi=300, bbox_inches='tight')
print(f"\nグラフを 'InfectionSimulation_Comparison.png' として保存しました")