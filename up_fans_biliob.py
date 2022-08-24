import requests as rq
import pandas as pd
from datetime import datetime
import arrow
import os
from pytz import timezone
from pyquery import PyQuery as pq

time=datetime.now(timezone('Asia/Shanghai')).strftime('%Y-%m-%d::%H')
#df=pd.DataFrame(index=[time])
df=pd.read_csv('bili_fans/up_fans.csv',index_col=[0])
df.loc[time]=[0]*len(df.columns)
header={
	'Connection':'keep-alive', 
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36', 
	'Accept':'*/*', 
	'Accept-Encoding':'gzip, deflate', 
	'Accept-Language':'zh-CN,zh;q=0.9'
}

def spider():
	res=rq.get('https://zeroroku.com/_next/data/sW-UJcYRbybO0jl2Ul68z/bilibili/rank/rate1/desc.json?field=rate1&order=desc',headers=header,timeout=(60,60)).json()
	return res['pageProps']['data']
	

def proc():
	data=spider()
	for i in data[:21]:
		name=i['name']
		uid=i['mid']
		cRate=i['stats']['rate1']
# 		name,uid=doc(f'.gap-3:eq({i}) .flex-1 div').text().split(' UID: ')
# 		cRate=doc(f'.gap-3:eq({i}) .flex-shrink div').text().replace(',','')
		if name not in df.columns:
			df[name]=[0]*len(df.index)
			df[name]['mid']=uid
		df[name][time]=cRate
		# if not os.path.exists(f'pic_down_biliob/{i["name"]}.jpg'):
		# 	with open(f'pic_down_biliob/{i["name"]}.jpg','wb') as f:
		# 		f.write(rq.get(i['face']).content)
		print(name,cRate)

if __name__ == '__main__':
	
	proc()

	df=df.drop_duplicates()
	df.to_csv('bili_fans/up_fans.csv',header=True,index=True)
