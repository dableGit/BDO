import requests
import json
import pandas as pd

def get_item_id(name: str) -> str:
    # GET BDO id of an item from the item name
    items = pd.read_csv('BDO Items.csv', sep=';')
    condition = items.Name.isin([name])
    return items[condition].Index.values[0]

def get_item_name(id: str) -> str:
    # GET BDO name of an item from the item id
    items = pd.read_csv('BDO Items.csv', sep=';')
    condition = items.Index.isin([id])
    return items[condition].Name.values[0]


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


def get_prices(name: str) -> pd.DataFrame:
    # Returns full data from endpoint GetWorldMarketSubList as a dataframe
    idx = get_item_id(name)
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
    # print(df.info())
    # Convert unix timestamp to datetime
    df['Last sale time'] = pd.to_datetime(pd.to_numeric(df['Last sale time']), unit='s')
    return df

def get_category(main, sub):
    url = 'https://eu-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketList'
    myjson = {
        "keyType": 0,
        "mainCategory": main,
        "subCategory": sub
    }
    resp = convert_resp(requests.post(url, data=myjson).text)
    # print(resp)
    columns = [
        'ItemID', 'Current stock', 'Total Trades', 'Base Price'
    ]
    df = pd.DataFrame(resp, columns=columns)
    df['Name'] = get_item_name(df['ItemID'])

# print(get_category(30,1))

def get_base_price(name: str) -> int:
    # Returns the base price of an unenhanced item
    df = get_prices(name)
    return int(df['Base Price'].values[0])


def get_price_list(name: str) -> list:
    # Returns a list of prices from 0 to PEN enhancement levels
    df = get_prices(name)
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



def get_bidding_info_arsha(idx, subkey=0):
    url = "https://api.arsha.io/v2/eu/GetBiddingInfoList?id=" + str(idx) + "&sid" + str(subkey)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    highest_buyorder = None
    lowest_sellorder = None
    LLowest_sellorder = None
    highest_buyorder = None
    both_none_flag  = 0
    for order in data['orders']:
        if order['sellers'] > 0:
            if highest_buyorder is None or order['price'] > highest_buyorder:
                highest_buyorder = order['price']
        elif order['buyers'] > 0:
            if lowest_sellorder is None or order['price'] < LLowest_sellorder:
                LLowest_sellorder = order['price']
    if LLowest_sellorder is None and highest_buyorder is None:
        both_none_flag = 1
    return (LLowest_sellorder, highest_buyorder, both_none_flag)

def get_bidding_info_arsha2(idx, subkey=0):
    url = "https://api.arsha.io/v2/eu/GetBiddingInfoList?id=" + str(idx) + "&sid" + str(subkey)
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return pd.json_normalize(data['orders'])

def get_minmax_orders(idx):
    orderbook = get_bidding_info_arsha2(idx)
    highest_buyorder = orderbook[(orderbook.sellers > 0)].price.max()
    lowest_buyorder = orderbook[(orderbook.sellers > 0)].price.min()
    highest_sellorder = orderbook[(orderbook.buyers > 0)].price.max()
    lowest_sellorder = orderbook[(orderbook.buyers > 0)].price.min()
    return (highest_buyorder, lowest_buyorder, highest_sellorder, lowest_sellorder)
            

def get_no_of_preorders(idx):
    orderbook = get_bidding_info_arsha2(idx)
    sorted = orderbook.sort_values(by=['price'], ascending=False)
    return sorted.sellers.values[0]



def get_bidding_info(idx, subkey=0):
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

def get_market_price_info(idx, subkey=0):
    # Returns a list of prices the last 90 days 
    url = 'https://eu-trade.naeu.playblackdesert.com/Trademarket/GetMarketPriceInfo'
    myjson = {
    "keyType": 0,
    "mainKey": idx,
    "subKey": subkey
    }
    resp = requests.post(url, data=myjson).text
    resp = json.loads(resp)
    resp = resp['resultMsg']
    resp = resp.split('-')    
    return [int(i) for i in resp]
    
print(get_prices("Crystallized Despair"))
# print(get_prices(get_item_name('8411')))

# print(get_bidding_info_arsha2(5408).sort_values(by=['price'], ascending=False))
# print(get_no_of_preorders(610448))