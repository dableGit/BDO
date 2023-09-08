# import pandas as pd
from prices import get_item_id, get_base_price, get_price_list
from chances import get_chance
from fs_costs import read_fs_costs

costs = read_fs_costs()

class BS_Weapon():

    def __init__(self, name):

        self.id = get_item_id(name)
        self.name = name
        self.category = 'Weapon BS'

        self.prices = get_price_list(name)

        MEM = get_base_price('Memory Fragment')
        CBSA = get_base_price('Concentrated Magical Black Stone (Armor)')
        SBCS = get_base_price('Sharp Black Crystal Shard')
        HBCS = get_base_price('Hard Black Crystal Shard')
        MopM = 5000000

        self.repair_low = 10*MEM
        self.mats_low = CBSA
        self.repair_high = 20*MEM
        self.mats_high = SBCS + HBCS + MopM

        self.levels = {
            1: '1', 2:'2', 3:'3', 4:'4', 5:'5',
            6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
            11: '11', 12: '12', 13: '13', 14: '14', 15: '15',
            16: 'PRI', 17: 'DUO', 18: 'TRI', 19: 'TET', 20: 'PEN',
        }

    # Get most profitable FS to enhance a specific level (or 0 if not profitable at all)
    def enhance(self, level):
        down = 0
        if level < 15:
            repair = self.repair_low
            mats = self.mats_low
        else:
            repair = self.repair_high
            mats = self.mats_high
        if level >= 17:
            down = self.prices[level] - self.prices[level-1]
            if down > cron(level) * 2000000:
                down = cron(level) * 2000000
                print(level, 'CRON!')
        best_fs = 0
        best_cost = -1
        for fs, fscost in enumerate(costs):            
            chance = get_chance(self.category, level, fs)
            fail = 1 - chance            
            cost = (chance*fscost + fail*(repair + down) + mats) / chance
            print(fs, cost)
            if (cost < best_cost) or (best_cost == -1):
                best_fs = fs
                best_cost = cost
        return (best_fs, int(best_cost/1000000))


def cron(level):
    if level == 17:
        return 100
    if level == 18:
        return 591
    if level == 19:
        return 3670

def bs_fs():
    bs = BS_Weapon("Blackstar Crescent Pendulum")
    bs.enhance(18)
    # print(bs.name)
    # print(bs.prices)
    # cumulated = 0
    # for level in range(20):
    #     fs, cost = bs.enhance(level)
    #     cumulated = cumulated + cost
    #     print(bs.levels[level+1], fs, cost, cumulated)

bs_fs()

