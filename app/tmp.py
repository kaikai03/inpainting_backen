###############################################
# 临时工作
import requests, json
import pandas as pd

pd.set_option('display.max_columns', 40)
pd.set_option('display.width', 3000)

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
# 临时工作 先心统计
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
# 临时工作 ris
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

## 获取ris报告内容
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
# 临时工作 patientinfo
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


######ris补充############################
abs(np.random.normal(10,6))
int(abs(np.random.normal(2,2))+1)

accession = 37659

tmp = []
for x in range(100):
    accession+= 1
    print('MR'+str(accession))
    ret = requests.get('https://baby3.drims.cn/map/getRis?ReportsDateTime=%s&AccessionNumber=%s' %
                       ('20201108-20201218','MR'+str(accession)), headers=header)
    reports = json.loads(ret.text)
    # reports
    if len(ret.text) < 30:
        print('error:', len(ret.text))
        continue
    tmp.extend(reports['data'])
    print(reports['data'][0]['ReportsDateTime'])
    print(reports['data'][0]['ReportsConclusion'])
    print(reports['data'][0]['ReportsEvidences'])
    time.sleep(abs(np.random.normal(10,6)))


# if reports['code']==1:
#     print('error:', reports['msg'])
#     continue

ris_pool.extend(tmp)

df_rises = pd.DataFrame(ris_pool)
df_rises.to_excel('C:\\Users\\fakeQ\Desktop\\er_test_rises.xlsx')


df_rises[['ReportsDateTime','ReportsConclusion','ReportsEvidences']]

# A47903488 2020-08-17 2020-08-20"
# bgdh=20200818G0043059"
################################lis
get_lis_report = "https://baby3.drims.cn/map/getLis?cardNumber=%s&start=%s&end=%s"
get_lis_detail = "https://baby3.drims.cn/map/getLisDetail?bgdh=%s"

ret = requests.get('https://baby3.drims.cn/map/getHis?jzlb=1&cardNumber=2021889', headers=header)
reports = json.loads(ret.text)
# 'https://baby3.drims.cn/map/getHis?jzlb=1&cardNumber=2021889'
# https://baby3.drims.cn/map/getLis?cardNumber=A06429687&start=2018-03-10&end=2020-12-16

visits_aggregation2 = df_visits[['cn','startTime','endTime']].groupby('cn')\
    .apply(lambda x: (min(x['startTime'])[0:10],max(x['endTime'])[0:10]))

lis_error = []
lis_pool = []
for ind, v in enumerate(visits_aggregation2.iteritems()):
    # if ind > 3:
    #     break

    car = v[0]
    t_ = v[1]
    print(ind, car, t_[0], t_[1])

    ret = requests.get(get_lis_report % (car, t_[0], t_[1]), headers=header)

    if ret.status_code != 200:
        print('error:', ret.status_code)
        lis_error.append((0, car, ret.status_code,ret.text))
        continue
    if len(ret.text) < 20:
        print('error:', len(ret.text))
        lis_error.append((0, car, ret.status_code, ret.text))
        if ret.text == None:
            ret = requests.get(get_lis_report % (car, t_[0], t_[1]), headers=header)
            if ret.status_code != 200:
                print('error:', ret.status_code)
                lis_error.append((0, car, ret.status_code, ret.text))
                continue
            if len(ret.text) < 20:
                print('error:', ret.status_code)
                lis_error.append((0, car, ret.status_code, ret.text))
                continue
        else:
            continue
    reports = json.loads(ret.text)
    if reports['code']!=0:
        print('error:', reports['msg'])
        lis_error.append((0, car, reports['code'], reports['msg']))
        continue

    lis_reports = reports['data']
    print('step1:---------------')
    for report in lis_reports:
        ret = requests.get(get_lis_detail % (report['BGDH']), headers=header)
        if ret.status_code != 200:
            print('error:', ret.status_code)
            lis_error.append((0, car, ret.status_code, ret.text))
            continue
        if len(ret.text) < 20:
            print('error:', len(ret.text))
            lis_error.append((0, car, ret.status_code, ret.text))
            continue
        details = json.loads(ret.text)
        if details['code'] != 0:
            print('error:', details['msg'])
            lis_error.append((0, car, details['code'], details['msg']))
            continue

        lis_details = details['data']
        for detail in lis_details:
            for key in report.keys():
                detail[key] = report[key]

    lis_pool.extend(lis_details)

    time.sleep(abs(np.random.normal(15,6)))
    print(car, 'finish')

    break

df_lises = pd.DataFrame(lis_pool)
df_lises.to_excel('C:\\Users\\fakeQ\Desktop\\er_test_lises.xlsx')


['A05258150','F28863775','B34169480','A00950041','A03026399','A000300380430','A06429687','A00169183','A41672463',
'B33912156','B34319768','B32317144','B49363056','B000900075191','B34567921','A10971911','A06574833','A42841687',
'A08128343']