# 原始数据没有了地区，这里补充一下

import os
import pandas as pd
import requests

DIR_PATH = './cloudflare-better-ip-main/cloudflare/'
RES_PATH = './result/'
ONLYIP_PATH = './resip/'

files = [file for file in os.listdir(DIR_PATH) if file.endswith('.txt')]

data_frames = []
for idx, txtfile in enumerate(files):
    new_data = pd.read_csv(DIR_PATH + txtfile, sep='|', header=None, names=['IP1', 'IP2', 'Region', 'Ping', 'Provider', 'Timestamp'])
    data_frames.append(new_data)

data = pd.concat(data_frames)
data = data.apply(lambda x: x.str.strip())

onlyips = data['IP1'].drop_duplicates().apply(lambda x: x.split(':')[0]).to_list()
print(f'共有{len(onlyips)}个ip')

def ipinfoapi(ips:list):
    url = 'http://ip-api.com/batch'
    ips_dict = [{'query': ip, "fields": "city,country,countryCode,isp,org,as,query"} for ip in ips]
    resp = requests.post(url, json=ips_dict)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f'获取ip信息失败，状态码：{resp.status_code}')

def get_ip_info(ips):
    ipsinfo = []
    
    for i in range(0, len(ips), 100):
        count = min(i+100, len(ips))
        ipsinfo += ipinfoapi(ips[i:i+100])
        print(f'已获取{count}个ip信息')
    return ipsinfo

def process_ipinfo(ipinfo):
    # df = pd.DataFrame(ipinfo)
    grouped = pd.DataFrame(ipinfo).groupby('countryCode')
    for countryCode, group in grouped:
        only_ip = group['query'].drop_duplicates()
        only_ip.to_csv(ONLYIP_PATH + countryCode + '.txt', header=None, index=False)

process_ipinfo(get_ip_info(onlyips))
print('已完成')
