import requests as rq
import pandas as pd
from datetime import datetime
import arrow
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

def spider():
	return rq.get('https://api.biliob.com/rank/fans-increase-rate',headers=header).json()

def proc():
	all_data=spider()
	data=all_data['content']
	for i in data:
		if i['name'] not in df.columns:
			df[i['name']]=[0]*len(df.index)
		df[i['name']][time]=i['cRate']
		df[i['name']]['mid']=i['mid']
		# if not os.path.exists(f'pic_up_biliob/{i["name"]}.jpg'):
		# 	with open(f'pic_up_biliob/{i["name"]}.jpg','wb') as f:
		# 		f.write(rq.get(i['face']).content)
		print(i['name'])

if __name__ == '__main__':
	
	proc()

	df=df.drop_duplicates()
	df.to_csv('bili_fans/up_fans.csv',header=True,index=True)
