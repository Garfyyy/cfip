import os
import pandas as pd

DIR_PATH = './cloudflare-better-ip-main/cloudflare/'
RES_PATH = './result/'

files = [file for file in os.listdir(DIR_PATH) if file.endswith('.txt')]

data_frames = []
for idx, txtfile in enumerate(files):
    new_data = pd.read_csv(DIR_PATH + txtfile, sep='|', header=None, names=['IP1', 'IP2', 'Region', 'Ping', 'Provider', 'Timestamp'])
    data_frames.append(new_data)

data = pd.concat(data_frames)
data = data.apply(lambda x: x.str.strip())

grouped_data = data.groupby('Region')
for region, group in grouped_data:
    group['Ping'] = group['Ping'].replace('ms', '', regex=True).astype(int)
    group = group.sort_values(by=['Ping'])
    group = group[~(group['Ping'] == 0)]
    group['Ping'] = group['Ping'].astype(str) + 'ms'
    group.to_csv(RES_PATH + region + '.txt', sep='\t', header=None, index=False)
