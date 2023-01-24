import pandas as pd
from prices import get_item_id, get_base_price, get_price_list
from fs_costs import costs


class Armor():

    def __init__(self, name, repair_low, mats_low, repair_high, mats_high):

        self.id = get_item_id(name)
        self.name = name

        self.prices = get_price_list(name)

        self.repair_low = repair_low
        self.mats_low = mats_low
        self.repair_high = repair_high
        self.mats_high = mats_high

        self.chances = pd.read_csv('Armor_FS.csv', sep=';')
        self.chances = self.chances / 100

        self.levels = {
            6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
            11: '11', 12: '12', 13: '13', 14: '14', 15: '15',
            16: 'PRI', 17: 'DUO', 18: 'TRI', 19: 'TET', 20: 'PEN',
        }

        # Starting from +7
        self.base_chance = [0.256410, 0.172413, 0.117647, 0.076923, 0.0625, 0.05,
                            0.04, 0.028571, 0.02, 0.117647, 0.076923, 0.0625, 0.02, 0.003]
        self.soft_cap = [18, 31, 50, 82, 102, 130, 165, 236, 340, 50, 82, 102, 340, 2324]

    # Get enhancement success chance based on enh. level (0-20) and failstack
    # Get enhancement success chance based on enh. level and failstack
    def get_chance(self, level, fs):
        if level <= 6:
            return 1
        if level == 7:
            return 0.9
        corr_level = level - 8
        if fs <= self.soft_cap[corr_level]:
            return self.base_chance[corr_level] + fs * self.base_chance[corr_level] / 10
        else:
            return self.base_chance[corr_level] + self.soft_cap[corr_level] * self.base_chance[corr_level] / 10 + (
                fs - self.soft_cap[corr_level]) * self.base_chance[corr_level] / 50

    # Get most profitable FS to enhance a specific level (or 0 if not profitable at all)
    def enhance(self, level):
        if level <= 6:
            return 1
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


def armor_fs():
    BSA = get_base_price('Black Stone (Armor)')
    # BSW = get_base_prices('Black Stone (Weapon)')
    MEM = get_base_price('Memory Fragment')
    CBSA = get_base_price('Concentrated Magical Black Stone (Armor)')

    red_nose = Armor("Red Nose's Armor", 5*MEM, BSA, 10*MEM, CBSA)
    print('Red Nose')
    for level in range(6, 21):
        print(red_nose.levels[level], red_nose.enhance(level))

    Lemoria = 900000
    print('Lemoria')
    lemoria = Armor("Lemoria Armor", 0.5*Lemoria, BSA, Lemoria, CBSA)
    for level in range(6, 21):
        print(lemoria.levels[level], lemoria.enhance(level))
    # print(armor.enhance(19))


armor_fs()
