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





###############################################
# 临时工作
import pandas as pd
pd.set_option('display.max_columns', 40)
pd.set_option('display.width', 300)

excel = 'F:\\Cache\\qt\\35331963\\FileRecv\\出院为2020.xlsx'
df = pd.read_excel(excel,sheet_name='数据')

indexes = ['房间隔缺损修补术','室间隔缺损修补术','经皮房间隔缺损封堵术','经皮动脉导管未闭封堵术','二尖瓣成形术','经皮室间隔缺损封堵术','蓝光照射治疗','经胸室间隔缺损闭式封堵术','二尖瓣修补术','房间隔缺损闭式封堵术','心血管造影术','动脉导管未闭结扎术','主动脉缩窄术','完全型心内膜垫缺损矫治术','心电生理检查','卵圆孔未闭修补术','三尖瓣修补术','部分型肺静脉畸形引流矫治术','动脉导管结扎术','三尖瓣成形术','右室流出道疏通术','肺动脉球囊扩张成形术','动脉导管未闭切断缝合术','肺动脉瓣探查术','术中心脏电生理检查','关胸术','肺叶切除术','封堵器取出术','肺修补术','心包穿刺术']

for item in indexes:
    ct = df[(df['主手术名称']==item) | (df['手术2']==item)| (df['手术3']==item)| (df['手术4']==item)].shape[0]
    print(item,ct)


###############################################
# 临时工作
import pandas as pd
import requests, json
import time

excel = 'C:\\Users\\fakeQ\Desktop\\research_sx_er_test_patient.xlsx'

header = {'Content-Type': 'application/json'}
get_time_url = 'https://baby3.drims.cn/map/getHis?jzlb=1&cardNumber=%s'

get_report_url = 'https://baby3.drims.cn/map/getRis?ReportsDateTime=%s&AdmissionID=%s'


df = pd.read_excel(excel)
cn = df[['name', 'cardNumber']].dropna()

## 获取流水记录
visits_pool = []
for c in cn.iterrows():
    ind = c[0]
    name = c[1][0]
    car = c[1][1]
    print(ind,name,car)
    # if ind < 7:
    #     continue
    ret = requests.get(get_time_url % car, headers=header)
    if ret.status_code != 200:
        print('error:',ret.status_code)
        continue
    if len(ret.text) < 10:
        print('error:', len(ret.text))
        continue
    visits = json.loads(ret.text)
    for visit in visits:
        visit['name'] = c[1][0]
        visit['cn'] = c[1][1]
    visits_pool.extend(visits)

    time.sleep(4.0)
    print(c[0], 'finish')


df_visits = pd.DataFrame(visits_pool)
df_visits.to_excel('C:\\Users\\fakeQ\Desktop\\er_test_visits.xlsx')

# df_visits.reset_index()
# ret_test = requests.get(get_report_url % ('20190911-20190912', 'A000300314971'), headers=header)
# ris_test = json.loads(ret_test.text)
#
# len(ris_test.text)

visits_aggregation = df_visits[['cn','startTime','endTime']].groupby('cn')\
    .apply(lambda x: min(x['startTime'])[0:10].replace('-','')
                     +'-'+max(x['endTime'])[0:10].replace('-',''))

## 获取报告内容
ris_pool = []
for ind, v in enumerate(visits_aggregation.iteritems()):
    car = v[0]
    t_ = v[1]
    print(ind, car, t_)
    # if ind < 7:
    #     continue
    ret = requests.get(get_report_url % (t_, car), headers=header)
    if ret.status_code != 200:
        print('error:', ret.status_code)
        continue
    if len(ret.text) < 10:
        print('error:', len(ret.text))
        continue
    reports = json.loads(ret.text)
    if reports['code']==1:
        print('error:', reports['msg'])
        continue

    ris_pool.extend(reports['data'])

    time.sleep(4.0)
    print(car, 'finish')

    # if ind >2:
    #     break

df_rises = pd.DataFrame(ris_pool)
df_rises.to_excel('C:\\Users\\fakeQ\Desktop\\er_test_rises.xlsx')

###############################################
# 临时工作
import pandas as pd
import requests, json
import time
import numpy as np

np.round(np.abs(np.random.normal(6, 4)), 2)

excel = 'C:\\Users\\fakeQ\Desktop\\research_sx_er_test_patient.xlsx'

header = {'Content-Type': 'application/json'}
get_p_info = 'https://baby3.drims.cn/map/getOracle?viewName=et_patientinfo&cardNo=%s'

get_records = 'https://baby3.drims.cn/map/getOracle?viewName=et_sfxx&cardNo=%s'



df = pd.read_excel(excel)
cn = df[['name', 'cardNo']].dropna()



ret = requests.get(get_p_info % ('060021192275'), headers=header)
reports = json.loads(ret.text)
