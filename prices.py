import requests
import json
import pandas as pd
# from datetime import datetime


def get_prices(idx):
    url = "https://eu-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketSubList"
    myjson = {
        "keyType": 0,
        "mainKey": idx
    }

    resp = convert_resp(requests.post(url, data=myjson))
    headers = ['ItemID', 'Enhance min', 'Enhance max', 'Base Price', 'Current Stock',
               'Total Trades', 'Price hardcap min', 'Price hardcap max', 'Last sale price', 'Last sale time']
    df = pd.DataFrame(resp, columns=headers)
    df['Last sale time'] = pd.to_datetime(df['Last sale time'], unit='s')
    return df

def get_price(idx):
    df = get_prices(idx)
    base = int(df['Base Price'].values[0])
    last = int(df['Last sale price'].values[0])
    return int((base + last) / 2)


def get_bidding_info(idx, subkey):
    url = "https://eu-trade.naeu.playblackdesert.com/Trademarket/GetBiddingInfoList"
    myjson = {
        "keyType": 0,
        "mainKey": idx,
        "subKey": subkey
    }
    headers = {
        # 'Content-Type': 'application/json',
        # 'User-Agent': 'BlackDesert'
    }

    x = requests.post(url, headers=headers, data=myjson)
    print(x.text)
    resp = convert_resp(x)
    headers = ['Price', '# Sell Orders', '# Buy Orders']
    df = pd.DataFrame(resp, columns=headers)
    return df


def convert_resp(resp):
    mydata = json.loads(resp.text)
    mydata = mydata['resultMsg']
    new_list = []
    for resp in mydata.split('|')[:-1]:
        myresp = resp.split('-')
        new_list.append(myresp)
    return new_list


# GET BDO id of an item from the item name
def get_item_id(name):
    prices = pd.read_csv('BDO Items.csv', sep=';')
    cond = prices.Name.isin([name])
    return prices[cond].Index.values[0]


