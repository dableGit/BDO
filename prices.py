import requests
import json
import pandas as pd


def get_item_id(name: str) -> str:
    # GET BDO id of an item from the item name
    items = pd.read_csv('BDO Items.csv', sep=';')
    condition = items.Name.isin([name])
    return items[condition].Index.values[0]


def convert_resp(resp: str) -> list:
    # Convert an API response to a list of lists
    # Check https://developers.veliainn.com/ for example response structure
    mydata = json.loads(resp)
    mydata = mydata['resultMsg']
    new_list = []
    for resp in mydata.split('|')[:-1]:
        myresp = resp.split('-')
        new_list.append(myresp)
    return new_list


def get_prices(idx: str) -> pd.DataFrame:
    # Returns full data from endpoint GetWorldMarketSubList as a dataframe
    url = "https://eu-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketSubList"
    myjson = {
        "keyType": 0,
        "mainKey": idx
    }
    resp = convert_resp(requests.post(url, data=myjson).text)
    columns = [
        'ItemID', 'Enhance min', 'Enhance max', 'Base Price', 'Current Stock',
        'Total Trades', 'Price hardcap min', 'Price hardcap max', 'Last sale price',
        'Last sale time'
    ]
    df = pd.DataFrame(resp, columns=columns)
    # Convert unix timestamp to datetime
    df['Last sale time'] = pd.to_datetime(df['Last sale time'], unit='s')
    return df


def get_base_price(name: str) -> int:
    # Returns the base price of an unenhanced item
    idx = get_item_id(name)
    df = get_prices(idx)
    return int(df['Base Price'].values[0])


def get_price_list(name: str) -> list:
    # Returns a list of prices from 0 to PEN enhancement levels
    idx = get_item_id(name)
    df = get_prices(idx)
    pricelist = []
    for i in range(6):
        pricelist.append(int(df['Base Price'].values[0]))
    for i in range(6, 10):
        pricelist.append(int(df['Base Price'].values[1]))
    for i in range(10, 13):
        pricelist.append(int(df['Base Price'].values[2]))
    for i in range(13, 21):
        pricelist.append(int(df['Base Price'].values[i-10]))
    return pricelist


def get_bidding_info(idx, subkey):
    # Endpoint does not work at the moment
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
    resp = convert_resp(x.text)
    headers = ['Price', '# Sell Orders', '# Buy Orders']
    df = pd.DataFrame(resp, columns=headers)
    return df
