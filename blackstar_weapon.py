# import pandas as pd
from prices import get_item_id, get_base_price, get_price_list
from fs_costs import costs


class BS_Weapon():

    def __init__(self, name):

        self.id = get_item_id(name)
        self.name = name

        self.prices = get_price_list(name)

        MEM = get_base_price('Memory Fragment')
        CBSA = get_base_price('Concentrated Magical Black Stone (Armor)')
        SBCS = get_base_price('Sharp Black Crystal Shard')
        HBCS = get_base_price('Hard Black Crystal Shard')
        MopM = 5000000

        self.repair_low = 10*MEM
        self.mats_low = CBSA
        self.repair_high = SBCS + HBCS + MopM
        self.mats_high = 20*MEM

        self.levels = {
            6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
            11: '11', 12: '12', 13: '13', 14: '14', 15: '15',
            16: 'PRI', 17: 'DUO', 18: 'TRI', 19: 'TET', 20: 'PEN',
        }

        # Starting from +8
        self.base_chance = [0.204081, 0.142857, 0.1, 0.066666, 0.04,
                            0.025, 0.02, 0.130769, 0.106250, 0.034, 0.0051, 0.002]
        self.soft_cap = [25, 40, 60, 96, 165, 270, 340, 44, 56, 196, 1363, 3490]

    # Get enhancement success chance based on enh. level and failstack
    def get_chance(self, level, fs):
        if level <= 7:
            return 1
        if level == 8:
            return 0.9
        corr_level = level - 9
        if fs <= self.soft_cap[corr_level]:
            return self.base_chance[corr_level] + fs * self.base_chance[corr_level] / 10
        else:
            return self.base_chance[corr_level] + self.soft_cap[corr_level] * self.base_chance[corr_level] / 10 + (
                fs - self.soft_cap[corr_level]) * self.base_chance[corr_level] / 50

    # Get most profitable FS to enhance a specific level (or 0 if not profitable at all)
    def enhance(self, level):
        if level <= 8:
            return (0, self.mats_low/1000000)
        down = 0
        if level <= 15:
            repair = self.repair_low
            mats = self.mats_low
        else:
            repair = self.repair_high
            mats = self.mats_high
        if level > 17:
            down = self.prices[level-1] - self.prices[level-2]
        best_fs = 0
        best_cost = -1
        for fs, fscost in enumerate(costs):
            chance = self.get_chance(level, fs)
            fail = 1 - chance
            # cost = (fscost + repair + mats + down) / chance
            cost = (chance*fscost + fail*(repair + down) + mats) / chance
            # print(fs, int(cost/1000000), chance)
            if (cost < best_cost) or (best_cost == -1):
                best_fs = fs
                best_cost = cost
        return (best_fs, int(best_cost/1000000))


def bs_fs():
    bs = BS_Weapon("Blackstar Crescent Pendulum")
    print(bs.name)
    for level in range(8, 21):
        print(bs.levels[level], bs.enhance(level))


bs_fs()
