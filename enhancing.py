import pandas as pd
from prices import get_item_id, get_prices, get_price

BSA = get_price(get_item_id('Black Stone (Armor)'))
# BSW = get_prices(get_item_id('Black Stone (Weapon)'))
# MEM = get_prices(get_item_id('Memory Fragment'))
# CBSA = get_prices(get_item_id('Concentrated Magical Black Stone (Armor)'))
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

# Calc FS Cost based on +14 Reblath enhancing
repair = r_base / 2
for fs in range(1, 121):
    stake = BSA + costs[-1]
    c_succ = df['15'][fs-1]
    c_fail = 1 - c_succ
    cost = (stake + c_fail * repair + c_succ * reset)/c_fail
    costs.append(cost)

# for i,cost in enumerate(costs):
#     print(i, int(cost/1000))


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

s = pd.Series(costs)
s.astype('int64').to_csv('test.csv')


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


class Accessory():

    def __init__(self, name):

        self.id = get_item_id(name)
        self.name = name

        df = get_prices(self.id)
        self.prices = [int(df['Base Price'].values[i]) for i in range(6)]

        self.base_chance = [0, 0.25, 0.1, 0.075, 0.025, 0.005]
        self.soft_cap = [0, 18, 40, 44, 110, 330]

    # Get enhancement success chance based on enh. level and failstack
    def get_chance(self, level, fs):
        if fs <= self.soft_cap[level]:
            return self.base_chance[level] + fs * self.base_chance[level] / 10
        else:
            return self.base_chance[level] + self.soft_cap[level] * self.base_chance[level] / 10 + (
                fs - self.soft_cap[level]) * self.base_chance[level] / 50

    # Get most profitable FS to enhance a specific level (or 0 if not profitable at all)
    def enhance(self, level):
        best_fs = 0
        best_profit = 0
        stake = self.prices[0] + self.prices[level-1]        
        for fs, cost in enumerate(costs):
            chance = self.get_chance(level, fs)
            profit = self.prices[level] - cost - stake / chance
            if profit > best_profit:
                best_fs = fs
                best_profit = profit
        return (level, best_fs, int(best_profit/1000000))

    def profits(self):
        print(self.name)
        print(self.enhance(1))
        print(self.enhance(2))
        print(self.enhance(3))


items = [
    "Laytenn's Power Stone",
    'Ogre Ring',
    'Tungrad Necklace',
    'Revived Lunar Necklace',
    'Deboreka Necklace',

    'Forest Ronaros Ring',
    'Ring of Crescent Guardian',
    'Eye of the Ruins Ring',
    'Ominous Ring',
    'Tungrad Ring',

    'Narc Ear Accessory',
    'Ethereal Earring',
    'Tungrad Earring',
    'Black Distortion Earring',

    "Orkinrad's Belt",
    "Basilisk's Belt",
    "Valtarra Eclipsed Belt",
    "Tungrad Belt",
    "Turo's Belt",
    "Deboreka Belt",
]

data = {}
for item in items:
    acc = Accessory(item)
    PRI = acc.enhance(1)
    DUO = acc.enhance(2)
    TRI = acc.enhance(3)
    row = [PRI[1], PRI[2], DUO[1], DUO[2], TRI[1], TRI[2]]
    data[acc.name] = row
    # acc.profits()

# data = {'acc1': [0, 0, 40, 20, 44, 100], 'acc2': [26, 10, 40, 30, 44, 80]}
columns = ['PRI_FS', 'PRI_profit', 'DUO_FS', 'DUO_profit', 'TRI_FS', 'TRI_profit']
df = pd.DataFrame.from_dict(data, orient='index', columns=columns)
df['total_profit'] = df['PRI_profit'] + df['DUO_profit'] + df['TRI_profit']
print(df)