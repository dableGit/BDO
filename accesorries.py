import pandas as pd
from prices import get_item_id, get_prices, get_market_price_info
from fs_costs import read_fs_costs

costs = read_fs_costs()

class Accessory():

    def __init__(self, name):

        self.id = get_item_id(name)
        self.name = name

        df = get_prices(name)
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

    # def enhance(self,level):
    #     stake = self.prices[0] + self.prices[level-1]
    #     success = self.prices[level]
    #     soft_cap = self.soft_cap[level]
        # for fs, cost in enumerate(costs):
        #     chance = self.get_chance(level, fs)
        #     profit = self.prices[level] - cost - stake / chance


        
    # Get most profitable FS to enhance a specific level
    def optimal_enhance(self, level):
        best_fs = 0
        best_profit = -10000000000
        stake = self.prices[0] + self.prices[level-1]
        for fs, cost in enumerate(costs):
            chance = self.get_chance(level, fs)
            profit = self.prices[level] - cost - stake / chance
            if profit > best_profit:
                best_fs = fs
                best_profit = profit
        return (best_fs, int(best_profit/1000000))

    def profits(self):
        print(self.name)
        print(self.optimal_enhance(1))
        print(self.optimal_enhance(2))
        print(self.optimal_enhance(3))


items = [
    "Serap's Necklace",
    "Sicil's Necklace",
    "Laytenn's Power Stone",
    'Ogre Ring',
    'Tungrad Necklace',
    'Revived Lunar Necklace',
    'Revived River Necklace',
    'Deboreka Necklace',

    'Forest Ronaros Ring',
    'Ring of Cadry Guardian',
    'Ring of Crescent Guardian',
    'Eye of the Ruins Ring',
    'Ominous Ring',
    'Tungrad Ring',

    'Narc Ear Accessory',
    'Ethereal Earring',
    'Tungrad Earring',
    "Vaha's Dawn",
    'Black Distortion Earring',

    "Centaurus Belt",
    "Orkinrad's Belt",
    "Basilisk's Belt",
    "Valtarra Eclipsed Belt",
    "Tungrad Belt",
    "Turo's Belt",
    "Deboreka Belt",
]

items = [
    "Serap's Necklace",
    "Sicil's Necklace",]


def acc_profits():
    data = {}
    for item in items:
        acc = Accessory(item)
        PRI = acc.optimal_enhance(1)
        DUO = acc.optimal_enhance(2)
        TRI = acc.optimal_enhance(3)
        TET = acc.optimal_enhance(4)
        PEN = acc.optimal_enhance(5)
        row = [acc.prices[0], *PRI, *DUO, *TRI, *TET, *PEN]
        data[acc.name] = row

    columns = ['base_price', 'PRI_FS', 'PRI_profit', 'DUO_FS',
               'DUO_profit', 'TRI_FS', 'TRI_profit', 'TET_FS', 'TET_profit', 'PEN_FS', 'PEN_profit']
    df = pd.DataFrame.from_dict(data, orient='index', columns=columns)
    # df['PRI-TRI'] = df['PRI_profit'] + df['DUO_profit'] + df['TRI_profit']
    # df['DUO-TRI'] = df['DUO_profit'] + df['TRI_profit']
    # df['DUO-TET'] = df['DUO_profit'] + df['TRI_profit'] + df['TET_profit']

    print(df.sort_values(by='base_price', ascending=True))

def prices_overview():
    data = {}
    for item in items:
        data[item] = [] 
        for level in range(5):
            prices = get_market_price_info(get_item_id(item),level)
            avg = sum(prices)/len(prices)
            last = prices[-1]
            data[item].append(round(last/avg, 2))
    print(pd.DataFrame.from_dict(data, orient='index'))

            

acc_profits()
# prices_overview()