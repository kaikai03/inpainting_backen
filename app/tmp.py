###############################################
# 临时工作
import requests, json
import pandas as pd

pd.set_option('display.max_columns', 40)
pd.set_option('display.width', 300)

excel = 'C:\\Users\\fakeQ\\Desktop\\心超报告语义分析后的数据.xlsx'
df = pd.read_excel(excel)
df['报告内容']

header = {'Content-Type': 'application/json'}
url = 'http://180.76.56.111:8383/api/echoCG'



def read_resualt(lis):
    dic_ = {}
    for _ in lis:
        dic_[_['Key']] = _['Value']
    return dic_


def NLP(origin):
    data = {"origin": origin}
    r = requests.post(url, headers=header, data=json.dumps(data))
    return read_resualt(json.loads(json.loads(r.text)))


deal_items = []
for index, text in enumerate(df['报告内容']):
    print(index, text)
    item = NLP(text)
    item["id"] = index
    deal_items.append(item)

test_items = deal_items[0:30]

df = pd.DataFrame(deal_items)
df = df.set_index('id')

df.to_excel('C:\\Users\\fakeQ\\Desktop\\deal.xlsx')

with open('C:\\Users\\fakeQ\\Desktop\\deal_items.txt', 'w') as f:
    f.write(json.dumps(deal_items))