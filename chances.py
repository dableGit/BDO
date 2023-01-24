import pandas as pd

base_chances = pd.read_csv('chances.csv')
soft_caps = pd.read_csv('SoftCap.csv')

def get_chance(category, level, fs):
    # Get enhancement success chance of an item based on enh. level and failstack
    base_chance = base_chances[category][level]
    soft_cap = soft_caps[category][level]
    if base_chance == 1.0:
        return 1.0
    if base_chance == 0.9:
        return 0.9    
    if fs <= soft_cap:
        return base_chance + fs * base_chance / 10
    else:
        return base_chance + soft_cap * base_chance / 10 + (fs - soft_cap) * base_chance / 50


# cat = 'Armor WBG'
# print(get_chance(cat,1,20))