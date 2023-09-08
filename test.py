import requests
import json
import pandas as pd

data = []

for id in range (20000,50000):

    url = f'https://api.arsha.io/v2/na/GetWorldMarketSubList?id={id}&lang=en'

    headers = {}
    payload = {}

    response = requests.request('GET', url, data=payload, headers=headers)
    resp = json.loads(response.text)
    if (resp[0]['name']):
        entry = resp[0]
        my_dict = {'name':entry['name'], 'id':entry['id'], 'icon':entry['icon']}
        data.append(my_dict)

df = pd.DataFrame(data)
df.to_csv('test.csv', mode='a', header=False)

matrix = [[j for j in range(3)] for i in range(3)]
