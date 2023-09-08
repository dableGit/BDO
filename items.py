# JSON with all items listed on the central market
# https://apiv2.bdolytics.com/en/EU/market/central-market-data

### Market Categories
# main 1 - Main Hand
#   sub 1-20 Weapon Type (Longsword, Longbow, Amulet, Axe, ...)
# main 5 - Sub Weapon
# main 10 - Awakening Weapon
# main 15 - Armor
#   sub 1 - Helmet
#   sub 2 - Armor
#   sub 3 - Gloves
#   sub 4 - Shoes
# main 20 - Acessories
#   sub 1 - Rings
#   sub 2 - Necklaces
#   sub 3 - Earrings
#   sub 4 - Belts
# main 25 - Material
# main 30 - Enhancement/Upgrade
# main 35 - Consumables
# main 40 - Life Tools
# main 45 - Alchemy Stone
# main 50 - Magic Crystals
# main 55 - Pearl Items
# main 60 - Dye
# main 65 - Mount
# main 70 - Ship
# main 75 - Wagon
# main 80 - Furniture

### Grade Types
# 0 - White
# 1 - Green
# 2 - Blue
# 3 - Yellow
# 4 - Red

import os
from datetime import datetime

import requests
import json
import pandas as pd

items_filename = 'items.json'

def last_update_older_than_1day():
    try:
        last_updated = datetime.fromtimestamp(os.path.getmtime(items_filename))    
    except FileNotFoundError:
         return True
    diff = datetime.now() - last_updated
    return diff.days > 0


def update_item_list():
    # JSON with all items listed on the central market
    url = "https://apiv2.bdolytics.com/en/EU/market/central-market-data"
    raw_data = requests.get(url).text
    json_object = json.loads(raw_data)
    json_object = json_object['data']
    with open(items_filename, "w") as outfile:
            outfile.write(json.dumps(json_object))


def get_item_list():
    return pd.read_json('items.json') 


def get_item_id(name: str) -> str:
    # GET BDO id of an item from the item name
    items = get_item_list()
    condition = items.Name.isin([name])
    return items[condition].item_id.values[0]


def get_item_name(id: str) -> str:
    # GET BDO name of an item from the item id
    items = get_item_list()
    condition = items.Index.isin([id])
    return items[condition].name.values[0]


def print_blue_TRI_accs():
    # BIS for Melody of the Stars
    items = get_item_list()
    custom_columns = ['item_id', 'name', 'price', 'in_stock', 'total_trades','grade_type', 'enhancement_level', 'market_main_category', 'market_sub_category']
    items = items[custom_columns]
    condition = (items.market_main_category == 20) & (items.enhancement_level == 3) & (items.grade_type == 2) & (items.in_stock > 0)
    print(items[condition].sort_values(by=['price']))

def print_offins():
    # BIS for Melody of the Stars
    items = get_item_list()
    custom_columns = ['item_id', 'name', 'price', 'in_stock', 'total_trades','grade_type', 'enhancement_level', 'market_main_category', 'market_sub_category','fourteen_day_volume']
    items = items[custom_columns]
    condition = (items.name.str.contains("Urugon")) & (items.enhancement_level == 19)
    print(items[condition].sort_values(by=['market_sub_category']))


def print_pearl_items(orderby='fourteen_day_volume', length=50):
    items = get_item_list()
    custom_columns = ['item_id', 'name', 'price', 'in_stock', 'total_trades','fourteen_day_volume', 'volume_change', 'market_main_category']
    items = items[custom_columns]
    condition = (items.market_main_category == 55) & (items.name.str.contains('Premium Set'))
    print(items[condition].sort_values(by=[orderby], ascending=False).head(length))

def create_db():
    from app import app, db, Item
    items_df = get_item_list()
    with app.app_context():
        for idx, row in items_df.iterrows():
            # df= get_prices(row['item_id'])
            df = pd.DataFrame()

            item = Item(
                item_id=row['item_id'],
                name=row['name'],
                enhancement_level=row['enhancement_level'],
                market_main_category=row['market_main_category'],
                market_sub_category=row['market_sub_category'],
                grade_type=row['grade_type'],
                hardcap_min=df['hardcap min'],
                hardcap_max=df['hardcap max']
            )
            db.session.add(item)
        db.session.commit()
         


if last_update_older_than_1day():
     update_item_list()

print_offins()
# custom_columns = ['item_id', 'name', 'price', 'in_stock', 'total_trades','grade_type', 'enhancement_level', 'market_main_category', 'market_sub_category']
# items = items[custom_columns]