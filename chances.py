import pandas as pd

base_chances = pd.read_csv('chances.csv')
soft_caps = pd.read_csv('SoftCap.csv')

def get_chance(category : int, level : int, fs : int) -> float:
    # Get enhancement success chance of an item based on enh. level and failstack
    base_chance = base_chances[category][level]
    soft_cap = get_softcap(category, level)
    if base_chance == 1.0:
        return 1.0
    if base_chance == 0.9:
        return 0.9    
    if fs <= soft_cap:
        return base_chance + fs * base_chance / 10
    else:
        return base_chance + soft_cap * base_chance / 10 + (fs - soft_cap) * base_chance / 50


def get_softcap(category : int, level : int) -> int:
    return soft_caps[category][level]


if __name__ == '__main__':
    # cat = 'Armor FG'
    # print(get_chance(cat,15,20))

    cat = 'Weapon BS'
    level = 18
    print(get_chance(cat,level,163))
