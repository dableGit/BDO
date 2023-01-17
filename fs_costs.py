import pandas as pd
from prices import get_item_id, get_prices, get_price

BSA = get_price(get_item_id('Black Stone (Armor)'))
# BSW = get_prices(get_item_id('Black Stone (Weapon)'))
# MEM = get_prices(get_item_id('Memory Fragment'))
CBSA = get_price(get_item_id('Concentrated Magical Black Stone (Armor)'))
# CBSW = get_prices(get_item_id('Concentrated Magical Black Stone (Weapon)'))

r_base = 12900
reset = 100000

# Bheg prices
PEN = 15000000000
TET = 2740000000
TRI = 1280000000
DUO = 940000000
PRI = 855000000

# Grunil Helmet prices
g_base = 530000
g_six = 3060000
g_ten = 14900000
g_013 = 35100000
g_PRI = 48000000
g_DUO = 66000000
g_TRI = 107000000
g_TET = 525000000
g_PEN = 930000000

tax_rate = 0.84825

df = pd.read_csv('Armor_FS.csv', sep=';')
df = df / 100

costs = []
costs.append(0)

def bs_convert(fs):
    if fs == 5:
        return 5 * BSA
    elif fs == 10:
        return 12 * BSA
    elif fs == 15:
        return 21 * BSA
    elif fs == 20:
        return 33 * BSA
    elif fs == 25:
        return 53 * BSA
    elif fs == 30:
        return 84 * BSA
    else:
        return 0

def raw_fs_costs(mats, repair, downgrade):
    return mats + repair + downgrade


def chain():    
    costs[20] = bs_convert(20)
    # PRI Reblath
    costs[23] = costs[20] + raw_fs_costs(CBSA, r_base / 2, 0)
    costs[26] = costs[23] + raw_fs_costs(CBSA, r_base / 2, 0)
    costs[29] = costs[26] + raw_fs_costs(CBSA, r_base / 2, 0)
    costs[32] = costs[29] + raw_fs_costs(CBSA, r_base / 2, 0)
    # DUO Reblath
    costs[36] = costs[32] + raw_fs_costs(CBSA, r_base / 2, bs_convert(30) - bs_convert(25))
    costs[40] = costs[36] + raw_fs_costs(CBSA, r_base / 2, bs_convert(30) - bs_convert(25))
    costs[44] = costs[40] + raw_fs_costs(CBSA, r_base / 2, bs_convert(30) - bs_convert(25))
    # TRI Reblath
    costs[49] = costs[44] + raw_fs_costs(CBSA, r_base / 2, costs[40] - bs_convert(30))
    costs[54] = costs[49] + raw_fs_costs(CBSA, r_base / 2, costs[40] - bs_convert(30))
    costs[59] = costs[54] + raw_fs_costs(CBSA, r_base / 2, costs[40] - bs_convert(30))
    costs[64] = costs[59] + raw_fs_costs(CBSA, r_base / 2, costs[40] - bs_convert(30))
    costs[69] = costs[64] + raw_fs_costs(CBSA, r_base / 2, costs[40] - bs_convert(30))
    costs[74] = costs[69] + raw_fs_costs(CBSA, r_base / 2, costs[40] - bs_convert(30))
    costs[79] = costs[74] + raw_fs_costs(CBSA, r_base / 2, costs[40] - bs_convert(30))
    # TET Reblath
    costs[85] = costs[79] + raw_fs_costs(CBSA, r_base / 2, costs[54] - costs[40])
    costs[91] = costs[85] + raw_fs_costs(CBSA, r_base / 2, costs[54] - costs[40])
    costs[97] = costs[91] + raw_fs_costs(CBSA, r_base / 2, costs[54] - costs[40])
    costs[103] = costs[97] + raw_fs_costs(CBSA, r_base / 2, costs[54] - costs[40])
    costs[109] = costs[103] + raw_fs_costs(CBSA, r_base / 2, costs[54] - costs[40])
    costs[115] = costs[109] + raw_fs_costs(CBSA, r_base / 2, costs[54] - costs[40])

def chain2():
    fs = 20
    costs[fs] = bs_convert(fs)
    # PRI Reblath
    gain = 3
    costs[fs+gain] = (costs[fs] + CBSA) / (1 - df['DUO'][fs])
    fs = fs+gain
    costs[fs+gain] = (costs[fs] + CBSA) / (1 - df['DUO'][fs])
    costs[29] = (costs[26] + CBSA) / (1 - df['DUO'][26])
    costs[32] = (costs[29] + CBSA) / (1 - df['DUO'][29])
    # DUO Reblath
    costs[36] = (costs[32] + CBSA) / (1 - df['TRI'][32])
    costs[40] = (costs[36] + CBSA) / (1 - df['TRI'][36])
    costs[44] = (costs[40] + CBSA) / (1 - df['TRI'][40])
    # TRI Reblath
    costs[49] = (costs[44] + CBSA) / (1 - df['TET'][44])
    costs[54] = (costs[49] + CBSA) / (1 - df['TET'][49])
    costs[59] = (costs[54] + CBSA) / (1 - df['TET'][54])
    costs[64] = (costs[59] + CBSA) / (1 - df['TET'][59])
    costs[69] = (costs[64] + CBSA) / (1 - df['TET'][64])
    costs[74] = (costs[69] + CBSA) / (1 - df['TET'][69])
    costs[79] = (costs[74] + CBSA) / (1 - df['TET'][74])
    # TET Reblath
    costs[85] = (costs[79] + CBSA) / (1 - df['PEN'][79])
    costs[91] = (costs[85] + CBSA) / (1 - df['PEN'][85])
    costs[97] = (costs[91] + CBSA) / (1 - df['PEN'][91])
    costs[103] = (costs[97] + CBSA) / (1 - df['PEN'][97])
    costs[109] = (costs[103] + CBSA) / (1 - df['PEN'][103])
    costs[115] = (costs[109] + CBSA) / (1 - df['PEN'][109])

    
# Calc FS Cost based on +14 Reblath enhancing
def old_method():
    repair = r_base / 2
    for fs in range(1, 121):
        stake = BSA + costs[-1]
        c_succ = df['15'][fs-1]
        c_fail = 1 - c_succ
        cost = (stake + c_fail * repair + c_succ * reset)/c_fail
        costs.append(cost)

# Calc FS Cost based on +14 Reblath enhancing
# Calc acc. to https://github.com/ILikesCaviar/BDO_Enhancement_Tool
def old_method2():
    repair = r_base / 2
    for fs in range(1, 121):        
        c_succ = df['15'][fs-1]
        c_fail = 1 - c_succ
        cost = (BSA + c_fail * repair + c_succ *  (costs[-1] + reset))/c_fail
        costs.append(cost)


# Calc FS cost based on Armor enhancing
def fs_costs(stake, res_succ, res_fail, succ_chances, fs_gain):
    for fs, cost in enumerate(costs):
        if fs >= len(costs)-fs_gain:
            break
        adj_stake = stake + cost
        c_succ = succ_chances[fs]
        c_fail = 1 - c_succ
        new_cost = (adj_stake - c_succ * res_succ) / c_fail - res_fail
        if new_cost < costs[fs+fs_gain]:
            print(fs)
            costs[fs+fs_gain] = new_cost


# Reblath PRI -> DUO
# fs_costs(CBSA + costs[25], costs[30], costs[25], df['DUO'], 3, r_base)
# fs_costs(CBSA, 0, 0, df['DUO'], 3)
# Reblath DUO -> TRI
# fs_costs(CBSA + costs[30], costs[40], costs[25], df['TRI'], 4, r_base)
# Reblath TRI -> TET
# fs_costs(CBSA + costs[40], costs[50], costs[30], df['TET'], 5, r_base)


# print('Grunil PRI -> DUO')
# fs_costs(CBSA + g_PRI, g_DUO * 0.9, g_PRI - g_base, df['DUO'], 3)
# print('Grunil DUO -> TRI')
# fs_costs(CBSA + g_DUO, g_TRI * 0.9 ,g_PRI - g_base, df['TRI'], 4)
# print('Grunil TRI -> TET')
# fs_costs(CBSA + g_TRI, g_TET * 0.9, g_DUO - g_base, df['TET'], 5)


def boss_armor(stake, res_succ, res_fail, succ_chances, fs_gain):
    gainz = []
    for fs in range(121-fs_gain):
        adj_stake = stake + costs[fs]
        c_succ = succ_chances[fs]
        c_fail = 1 - c_succ
        adj_res_fail = costs[fs+fs_gain] + res_fail
        gain = -adj_stake + c_fail * adj_res_fail + c_succ * res_succ
        gainz.append(gain)
    return gainz

# boss_armor(CBSA + PRI, DUO, PRI - 10*Mem, df['DUO'], 3)
# boss_armor(CBSA + DUO, TRI, PRI - 10*Mem, df['TRI'], 4)
# boss_armor(CBSA + TRI, TET, DUO - 10*Mem, df['TET'], 5)

# for fs, cost in chain().items():
#     print(fs, int(cost/1000000))

def formula(fs):
    return int((0.0531 *fs*fs  - 1.4*fs + 9.3627)*1000000)

costs = [formula(fs) for fs in range(1,121)]

# old_method()
# chain2()

s = pd.Series(costs)
s.astype('int64').to_csv('test.csv')
