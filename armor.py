import pandas as pd
from prices import get_item_id, get_base_price, get_price_list, get_prices
from chances import get_chance
from fs_costs import read_fs_costs

costs = read_fs_costs()

class FallenGod():
    def __init__(self, name) -> None:
        self.name = name
        self.category = 'Armor FG'
        df = get_prices(name)              
        self.prices = pd.to_numeric(df['Base Price']).tolist()
        # print(self.prices)
        MEM = get_base_price('Memory Fragment')
        self.repair = 30*MEM
        self.mats = 35000000

    def cron(self, level):
        if level == 1:
            return 1500
        if level == 2:
            return 2100
        if level == 3:
            return 2700
        if level == 4:
            return 4000

    def enhance(self, lvl):
    # Get most profitable FS to enhance a specific level (or 0 if not profitable at all)
        down = 0
        level = lvl - 15
        if level >= 1: # For DUO or higher, respect downgrades
            down = self.prices[level] - self.prices[level-1]
            if down > self.cron(level) * 2000000:
                down = self.cron(level) * 2000000
                print(level, 'CRON!')
        best_fs = 0
        best_cost = -1
        for fs, fscost in enumerate(costs):
            chance = get_chance(self.category, lvl, fs)
            fail = 1 - chance            
            cost = (chance*fscost + fail*(self.repair + down) + self.mats) / chance            
            if (cost < best_cost) or (best_cost == -1):
                best_fs = fs
                best_cost = cost
        return (best_fs, int(best_cost/1000000))



class Armor():

    def __init__(self, name, cat, repair_low, mats_low, repair_high, mats_high):

        self.id = get_item_id(name)
        self.name = name
        self.category = cat

        self.prices = get_price_list(name)

        self.repair_low = repair_low
        self.mats_low = mats_low
        self.repair_high = repair_high
        self.mats_high = mats_high

        # self.chances = pd.read_csv('Armor_FS.csv', sep=';')
        # self.chances = self.chances / 100

        self.levels = {
            1: '1', 2:'2', 3:'3', 4:'4', 5:'5',
            6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
            11: '11', 12: '12', 13: '13', 14: '14', 15: '15',
            16: 'PRI', 17: 'DUO', 18: 'TRI', 19: 'TET', 20: 'PEN',
        }

 
    def enhance(self, level):
    # Get most profitable FS to enhance a specific level (or 0 if not profitable at all)
        # if level <= 6:
        #     return 1
        down = 0
        if level < 15:
            repair = self.repair_low
            mats = self.mats_low
        else:
            repair = self.repair_high
            mats = self.mats_high
        if level >= 17: # For TRI or higher, respect downgrades
            down = self.prices[level] - self.prices[level-1]
        best_fs = 0
        best_cost = -1
        for fs, fscost in enumerate(costs):
            chance = get_chance(self.category, level, fs)
            fail = 1 - chance            
            cost = (chance*fscost + fail*(repair + down) + mats) / chance            
            if (cost < best_cost) or (best_cost == -1):
                best_fs = fs
                best_cost = cost
        return (best_fs, int(best_cost/1000000))


def armor_fs():
    BSA = get_base_price('Black Stone (Armor)')
    # BSW = get_base_prices('Black Stone (Weapon)')
    MEM = get_base_price('Memory Fragment')
    CBSA = get_base_price('Concentrated Magical Black Stone (Armor)')

    red_nose = Armor("Red Nose's Armor", 'Armor WBG', 5*MEM, BSA, 10*MEM, CBSA)
    print('Red Nose')
    cumulated = 0
    for level in range(20):
        fs, cost = red_nose.enhance(level)
        cumulated = cumulated + cost
        print(red_nose.levels[level+1], fs, cost, cumulated)


def fallen_god():    
    print('Fallen God')
    fallenGod = FallenGod("Fallen God's Armor")
    for level in range(15,20):
        print(level-15, fallenGod.enhance(level))    


armor_fs()
