import requests as rq
import pandas as pd
from datetime import datetime
from pyquery import PyQuery as pq
import os
from pytz import timezone


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

def spider_json():
	res=rq.get('https://api.zeroroku.com/bilibili/rank?f=rate1&o=0',headers=header,timeout=(60,60)).json()
	return res
	
def spider():
	res=rq.get('https://zeroroku.com/bilibili/rank/rate1/desc',headers=header,timeout=(60,60)).text
	return res

def proc_json():
	data=spider_json()
	for i in data[:21]:
		name=i['name']
		uid=i['mid']
		cRate=abs(i['stats']['rate1'])
		if name not in df.columns:
			df[name]=[0]*len(df.index)
			df[name]['mid']=uid
		df[name][time]=cRate
		# if not os.path.exists(f'pic_down_biliob/{i["name"]}.jpg'):
		# 	with open(f'pic_down_biliob/{i["name"]}.jpg','wb') as f:
		# 		f.write(rq.get(i['face']).content)
		print(name,cRate)
	
	
# def proc():
# 	data=spider()
# 	for i in range(1,22):
# # 		name=i['name']
# # 		uid=i['mid']
# # 		cRate=abs(i['stats']['rate1'])
# 		doc = pq(data)
# 		uid=doc(f'.gap-3:eq({i}) .flex-1 div').text().replace('UID:','')
# 		name = doc(f'.gap-3:eq({i}) .flex-1 a').text()
# 		cRate=doc(f'.gap-3:eq({i}) .flex-shrink div').text()[1:].replace(',','')
# 		if name not in df.columns:
# 			df[name]=[0]*len(df.index)
# 			df[name]['mid']=uid
# 		df[name][time]=cRate
# 		# if not os.path.exists(f'pic_down_biliob/{i["name"]}.jpg'):
# 		# 	with open(f'pic_down_biliob/{i["name"]}.jpg','wb') as f:
# 		# 		f.write(rq.get(i['face']).content)
# 		print(name,cRate)

if __name__ == '__main__':

	proc_json()
	df=df.drop_duplicates()
	df.to_csv('bili_fans/up_fans.csv',header=True,index=True)

