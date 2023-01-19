import pandas as pd
from prices import get_item_id, get_prices, get_price
from fs_costs import costs


class Armor():

    def __init__(self, name, repair_low, mats_low, repair_high, mats_high):

        self.id = get_item_id(name)
        self.name = name

        df = get_prices(self.id)
        self.prices = []
        for i in range(6):
            self.prices.append(int(df['Base Price'].values[0]))
        for i in range(6,10):
            self.prices.append(int(df['Base Price'].values[1]))
        for i in range(10,13):
            self.prices.append(int(df['Base Price'].values[2]))
        for i in range(13,21):
            self.prices.append(int(df['Base Price'].values[i-10]))

        self.repair_low = repair_low
        self.mats_low = mats_low
        self.repair_high = repair_high
        self.mats_high = mats_high


        self.chances = pd.read_csv('Armor_FS.csv', sep=';')
        self.chances = self.chances / 100

        self.levels = {            
            6:'6', 7:'7', 8:'8', 9:'9', 10:'10',
            11:'11', 12:'12', 13:'13', 14:'14', 15:'15',
            16:'PRI', 17:'DUO', 18:'TRI', 19:'TET', 20:'PEN',
        }

    # Get enhancement success chance based on enh. level (0-20) and failstack
    def get_chance(self, level, fs):
        if level < 6:
            return 1 
        return self.chances[self.levels[level]][fs]

    # Get most profitable FS to enhance a specific level (or 0 if not profitable at all)
    def enhance(self, level):
        if level < 6:
            return 1
        down = 0
        if level < 15:
            repair = self.repair_low
            mats = self.mats_low
        else:
            repair = self.repair_high
            mats = self.mats_high
        if level >= 17:
            down = self.prices[level-1] - self.prices[level-2]
        best_fs = 0
        best_cost = 100000000000
        for fs, fscost in enumerate(costs):
            chance = self.get_chance(level, fs)
            cost = (fscost + repair + mats + down) / chance
            if cost < best_cost:
                best_fs = fs
                best_cost = cost
        return (level, best_fs, int(best_cost/1000000))

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
        best_profit = -1000000000
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
    # "Serap's Necklace",
    "Sicil's Necklace",
    "Laytenn's Power Stone",
    'Ogre Ring',
    # 'Tungrad Necklace',
    # 'Revived Lunar Necklace',
    # 'Revived River Necklace',
    # 'Deboreka Necklace',

    'Forest Ronaros Ring',
    'Ring of Cadry Guardian',
    'Ring of Crescent Guardian',
    'Eye of the Ruins Ring',
    # 'Ominous Ring',
    # 'Tungrad Ring',

    'Narc Ear Accessory',
    'Ethereal Earring',
    # 'Tungrad Earring',
    # 'Black Distortion Earring',

    "Centaurus Belt",
    # "Orkinrad's Belt",
    "Basilisk's Belt",
    "Valtarra Eclipsed Belt",
    # "Tungrad Belt",
    # "Turo's Belt",
    # "Deboreka Belt",
]

# data = {}
# for item in items:
#     acc = Accessory(item)
#     PRI = acc.enhance(1)
#     DUO = acc.enhance(2)
#     TRI = acc.enhance(3)
#     TET = acc.enhance(4)
#     row = [acc.prices[0], PRI[1], PRI[2], DUO[1], DUO[2], TRI[1], TRI[2], TET[1], TET[2]]
#     data[acc.name] = row
#     # acc.profits()

# columns = ['base_price', 'PRI_FS', 'PRI_profit', 'DUO_FS', 'DUO_profit', 'TRI_FS', 'TRI_profit', 'TET_FS', 'TET_profit']
# df = pd.DataFrame.from_dict(data, orient='index', columns=columns)
# df['PRI-TRI'] = df['PRI_profit'] + df['DUO_profit'] + df['TRI_profit']
# df['DUO-TRI'] = df['DUO_profit'] + df['TRI_profit']
# df['DUO-TET'] = df['DUO_profit'] + df['TRI_profit'] + df['TET_profit']

# print(df.sort_values(by='base_price', ascending=True))


BSA = get_price(get_item_id('Black Stone (Armor)'))
# BSW = get_prices(get_item_id('Black Stone (Weapon)'))
MEM = get_price(get_item_id('Memory Fragment'))
CBSA = get_price(get_item_id('Concentrated Magical Black Stone (Armor)'))
armor = Armor("Red Nose's Armor", 5*MEM, BSA, 10*MEM, CBSA)
for level in range(21):
    print(armor.enhance(level))
