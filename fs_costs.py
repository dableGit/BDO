import pandas as pd
from prices import get_base_price
from chances import get_chance

BSA = get_base_price('Black Stone (Armor)')
# BSW = get_base_price('Black Stone (Weapon)')
# MEM = get_base_price('Memory Fragment')
CBSA = get_base_price('Concentrated Magical Black Stone (Armor)')
# CBSW = get_base_price('Concentrated Magical Black Stone (Weapon)')

r_base = 12900
reset = 100000

def calc_fs_costs():
    costs = []
    costs.append(0)
    
    # Reblath +14 method simulation
    repair = r_base / 2
    for fs in range(1, 31):
        stake = BSA + costs[-1]        
        c_succ = get_chance('Armor WBG', 14, fs)
        c_fail = 1 - c_succ
        cost = (stake + c_fail * repair + c_succ * reset)/c_fail
        costs.append(cost)

    # Formula with estimated 100 fs cost of 400m
    for fs in range(31, 101):
        costs.append(int((0.05105 * fs*fs - 1.10476*fs)*1000000))
    
    # Formula with estimated 240 fs cost of 10b
    for fs in range(101, 241):
        costs.append(int((0.26905 * fs*fs - 22.905*fs)*1000000))

    s = pd.Series(costs, name='fs_costs')    
    s.astype('int64').to_csv('fs_costs.csv')

def read_fs_costs():
    df = pd.read_csv('fs_costs.csv')    
    return df['fs_costs'].to_list()


############################ WIP #################################
def bs_convert(fs):
    if fs == 5:
        return 5 * BSA
    elif fs == 10:
        return 12 * BSA
    elif fs == 15:
        return 21 * BSA
    elif fs == 20:
        return 33 * BSA
    elif fs == 25:
        return 53 * BSA
    elif fs == 30:
        return 84 * BSA
    else:
        return 0


# calc_fs_costs()
# costs = read_fs_costs()

def test_calc():
    
    # Cumulative failure cost is just cost of click (conc/blackstones) + fail (repair).
    # Success cost is:
    # The cost of lost PRIs (for DUOs)
    # The taxed cost of lost DUOs (for TRIs) less the taxed value of TRIs (path generates TRIs to market going to 40, or pre-tax TRIs going to 44).
    # Plus the previous step's cumulative failure cost, plus the cost of the click.
    # Cost of stack is (1-stack loss chance) * cumulative failure cost + stack loss chance * success cost

    costs = []
    costs.append(0)

    # Reblath +14 method simulation
    repair = r_base / 2
    for fs in range(1, 4):
        stake = BSA + costs[-1]        
        c_succ = get_chance('Armor WBG', 14, fs)
        c_fail = 1 - c_succ
        cost = (stake + c_fail * repair + c_succ * reset)/c_fail
        costs.append(cost)

    # Reblath DUO simulation
    repair = r_base
    for fs in range(4, 101):
        stake = CBSA + costs[-1]        
        c_succ = get_chance('Armor WBG', 17, fs)
        c_fail = 1 - c_succ
        cost = (stake + c_fail * repair)/c_fail/3
        costs.append(cost)

    # Export costs     
    s = pd.Series(costs, name='fs_costs')    
    s.astype('int64').to_csv('fs_test2.csv')

def reb_chances():
    for fs in range(20, 41):
             
        c_succ = get_chance('Armor WBG', 14, fs)
        print(1-c_succ)

# test_calc()
# print(get_chance('Armor WBG', 17, 20))