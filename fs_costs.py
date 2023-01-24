import pandas as pd
from prices import get_base_price

BSA = get_base_price('Black Stone (Armor)')
# BSW = get_base_price('Black Stone (Weapon)')
# MEM = get_base_price('Memory Fragment')
CBSA = get_base_price('Concentrated Magical Black Stone (Armor)')
# CBSW = get_base_price('Concentrated Magical Black Stone (Weapon)')

r_base = 12900
reset = 100000

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
def old_method(max=31):
    repair = r_base / 2
    for fs in range(1, max):
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
        cost = (BSA + c_fail * repair + c_succ * (costs[-1] + reset))/c_fail
        costs.append(cost)


def formula(fs):
    return int((0.0531 * fs*fs - 1.4*fs + 9.3627)*1000000)
    # return int((0.001 * fs*fs*fs - 0.0809 * fs*fs + 1.8713 * fs - 5.6911)*1000000)


def formula2():
    for fs in range(31, 101):
        costs.append(int((0.05105 * fs*fs - 1.10476*fs)*1000000))


def formula3():
    for fs in range(101, 241):
        costs.append(int((0.26905 * fs*fs - 22.905*fs)*1000000))

# costs = [formula(fs) for fs in range(1, 121)]


old_method()
formula2()
formula3()

s = pd.Series(costs)
s.astype('int64').to_csv('test.csv')

# print(BSA)
