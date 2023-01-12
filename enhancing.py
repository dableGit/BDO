import pandas as pd
from prices import get_item_id, get_prices, get_price
from fs_costs import costs


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
        best_profit = -100000000
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
    TET = acc.enhance(4)
    row = [acc.prices[0], PRI[1], PRI[2], DUO[1], DUO[2], TRI[1], TRI[2], TET[1], TET[2]]
    data[acc.name] = row
    # acc.profits()

# data = {'acc1': [0, 0, 40, 20, 44, 100], 'acc2': [26, 10, 40, 30, 44, 80]}
columns = ['base_price', 'PRI_FS', 'PRI_profit', 'DUO_FS', 'DUO_profit', 'TRI_FS', 'TRI_profit', 'TET_FS', 'TET_profit']
df = pd.DataFrame.from_dict(data, orient='index', columns=columns)
df['total_profit'] = df['PRI_profit'] + df['DUO_profit'] + df['TRI_profit']

print(df.sort_values(by='base_price', ascending=True))