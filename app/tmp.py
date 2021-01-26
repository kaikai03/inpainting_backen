###############################################
# 临时工作
import requests, json
import pandas as pd
import time
import numpy as np

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
    if ind < 255:continue
    print(ind,name,car)
    # if ind < 7:
    #     continue
    ret = requests.get(get_time_url % car, headers=header)
    if ret.status_code != 200:
        print('error:',ret.status_code)
        continue
    if len(ret.text) < 25:
        print('error:', len(ret.text))
        continue
    visits = json.loads(ret.text)["data"]
    for visit in visits:
        visit['name'] = name
        visit['cn'] = car
    visits_pool.extend(visits)

    time.sleep(1.5)
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
# https://baby3.drims.cn/map/getLis?cardNumber=B48793054&start=2020-02-25&end=2020-12-25

visits_aggregation2 = df_visits[['cn','startTime','endTime']].groupby('cn')\
    .apply(lambda x: (min(x['startTime'])[0:10],max(x['endTime'])[0:10]))

lis_error = []
lis_pool = []
for ind, v in enumerate(visits_aggregation2.iteritems()):
    if ind == 0:
        continue

    car = v[0]
    t_ = v[1]
    print(ind, car, t_[0], t_[1])

    ret = requests.get(get_lis_report % (car, t_[0], t_[1]), headers=header)

    if ret.status_code != 200:
        print('error:', ret.status_code)
        lis_error.append((0, car, ret.status_code,ret.text))
        continue
    if len(ret.text) < 40:
        print('error:', len(ret.text))
        lis_error.append((0, car, ret.status_code, ret.text))
        reports = json.loads(ret.text)
        if reports['code']==1 and reports['msg']=="连接超时！":
            print('retry----')
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
        time.sleep(abs(np.random.normal(5, 5)))
        continue

    lis_reports = reports['data']
    print('step1:---------------')
    for report in lis_reports:
        ret = requests.get(get_lis_detail % (report['bgdh']), headers=header)
        print(ret.text)
        if ret.status_code != 200:
            print('error1:', report['bgdh'], ret.status_code)
            lis_error.append((0, car, ret.status_code, ret.text))
            continue
        if len(ret.text) < 10:
            print('error2:', report['bgdh'], len(ret.text))
            lis_error.append((0, car, ret.status_code, ret.text))
            continue

        details = json.loads(ret.text)

        if details['code'] == 1 and details['msg'] == None:
            print('retry----', report['bgdh'])
            time.sleep(5)
            ret = requests.get(get_lis_detail % (report['bgdh']), headers=header)
            print(ret.text)
            details = json.loads(ret.text)
            if ret.status_code != 200:
                print('error3:', report['bgdh'], ret.status_code)
                lis_error.append((0, car, ret.status_code, ret.text))
                continue
            if len(ret.text) < 20:
                print('error4:', report['bgdh'], ret.status_code)
                lis_error.append((0, car, ret.status_code, ret.text))
                continue

        if details['code'] != 0:
            print('error5:', report['bgdh'], details)
            lis_error.append((0, car, details['code'], details))
            continue

        lis_details = details['data']
        for detail in lis_details:
            for key in report.keys():
                detail[key] = report[key]

        lis_pool.extend(lis_details)
        print(report['bgdh'],'sucess')
        time.sleep(1)

    time.sleep(abs(np.random.normal(5,5)))
    print(car, 'finish')

    break

df_lises = pd.DataFrame(lis_pool)
df_lises.to_excel('C:\\Users\\fakeQ\Desktop\\er_test_lises2.xlsx')


car_tmp = ['A05258150','F28863775','B34169480','A00950041','A03026399','A000300380430','A06429687','A00169183','A41672463',
'B33912156','B34319768','B32317144','B49363056','B000900075191','B34567921','A10971911','A06574833','A42841687',
'A08128343']

visits_pool2 = []
for ind, c in enumerate(car_tmp) :
    name = ''
    car = c
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
    visits = visits['data']
    for visit in visits:
        visit['cn'] = car

    visits_pool2.extend(visits)

    time.sleep(abs(np.random.normal(3,2)))
    print(c, 'finish')


df_lises2 = pd.DataFrame(lis_pool)
df_lises2.to_excel('C:\\Users\\fakeQ\Desktop\\er_test_lises2.xlsx')

df_visits2 = pd.DataFrame(visits_pool2)

visits_aggregation2 = df_visits2[['cn', 'startTime', 'endTime']].groupby('cn') \
    .apply(lambda x: (min(x['startTime'])[0:10], max(x['endTime'])[0:10]))



id_start=642
id_end=1045

pinfo_url_base='http://fbjy.sxfby.com:9087/babyHealth/patient/getSingelInfo?id=%d&pageSize=1&plat=1'
for i in np.linspace(id_start, id_end, id_end-id_start+1):
    r = requests.get(pinfo_url_base% int(i), headers=header)
    print(json.loads(r.text)['data']['cardNumber'])

cards=['E41723450','B49515865','A47503089','A49215443','A000300351889','A000300351889','A000100783971','A48933689','B49488764','A44408908','B48390722','A49261773','E47666151','A49789922','B49854779','A49282240','B4890325X','A49547501','SA31452053','A000300380576','A50090051','B43445691','E49427701','A48901855','A49650218','A47221532','A003100098927','A49706402','A49986643','E49432201','A47591744','A4925379X','A50090203','B50040393','A50040759','A50072865','B50048803','A50112281','A50039408','A000300398529','A003300040443','A000300400925','A000300398519','A000300398516','A000300357244','A000300400943','A50067206','A50109015','A000300397830','A50136857','B50045098','A50059441','E50081461','A50040636','A50096963','A5012897X','A50122914','B000900149378','A50078087','A50110059','A50637651','A000300398517','A000300385616','A5008695X','A002500027719','A003300040530','D50108516','B50075895','B50085276','B001900206568','A50614919','A50042252','B5062855X','B003300066521','A003300040422','A50058537','B000100510265','B001900210291','A50042236','F49777987','A50613721','A50087864','A000300397484','A50077439','B47135703','A000300398522','B003300066055','A50084997','A50087936','A50043562','A50077519','A50039889','A50130789','B50086041','A000300396192','B002710013997','E50068611','A5003392X','A000300401370','A50117103','A50087899','A000300397517','A000300387939','A50055926','A001900213151','B003500042050','B50107092','A5014323X','B50087909','A50131618','A000300346447','A50076815','A50039133','B5013084X','B000900148046','A50643867','A50039723','A5007166X','A000300385621','A50104564','A50106746','A50045170','A50085981','A000300400818','B001900210824','B50139975','B50140159','B50065734','A50041102','A000300399408','D50057501','A50087151','A002500028032','B000900154288','B50099723','A000300401251','B50104713','A000300402215','A50083214','A000300402214','A50098774','A002100112361','A000300385291','B50620988','B000600055863','A004300007652','A000300396087','A002500027397','A50040732','A005500119283','A000300394076','A000300392916','B000900154277','A50112820','E5008315X','A000300398298','A000300400978','A000300387229','A50621676','A50080208','A50122738','A5064750X','A50069279','A50072478','A50140119','A50073075','A50099646','A5008417X','A50054835','A50073067','A000300394021','B50123682','A50077463','A000300394561','A000300398686','A50645715','D5065404X','F50621023','A000300392885','B50129099','A50075804','A50105989','B50630617','A5010525X','A50087944','A49535973','A000300396680','A000300392759','A000300370734','A50148081','A001700191814','A000300402185','C5013811X','B50117573','B50134218','A50623380','B001100116298','A003100103281','D50068876','B50636824','A50082828','A50633538','B50066622','A50140039','D5007394X','B50066155','A50129921','B50114081','B50624305','A50128718','A000300395027','A000300397897','A000300385307','A50097659','A000300401377','A000300402238','A000300395021','A002100112201','B50657596','B50618538','B50657609','A50076858','A000300397777','A50630716','A002300086226','A003100098472','A000300401235','B44549222','E47610588','A50099670','A50111924','A50619322','A000300387014','A000300398653','SBM1659424','D50131898','A50648553','A50105460','A50107482','B50102996','A50103596','A50073139','A50114148','A000300387820','A50656529','A000300397919','A50112898','A50105604','A5009014X','B5065474X','A000300399429','A50081307','A5063491X','A002500032279','B50632620','A0003003399594','A000300399427','E50124564','A000300398327']