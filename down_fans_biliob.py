import requests as rq
import pandas as pd
from datetime import datetime
# from pyquery import PyQuery as pq
from sqlalchemy import create_engine
import os
from pytz import timezone

ip_port, user, password = eval(os.environ["mysql_157"])

time=datetime.now(timezone('Asia/Shanghai')).strftime('%Y-%m-%d::%H')
con = create_engine(f'mysql+pymysql://{user}:{password}@{ip_port}/Win_Dataprocuremen?charset=utf8')
#df=pd.DataFrame(index=[time])
# df=pd.read_csv('bili_fans/down_fans.csv',index_col=[0])
header={
	'Connection':'keep-alive', 
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36', 
	'Accept':'*/*', 
	'Accept-Encoding':'gzip, deflate', 
	'Accept-Language':'zh-CN,zh;q=0.9'
}

# df.loc[time]=[0]*len(df.columns)
def spider_json():
	res=rq.get('https://api.zeroroku.com/bilibili/rank?f=rate1&o=1&s=30',headers=header,timeout=(60,60)).json()
	return res
	
def spider():
	res=rq.get('https://zeroroku.com/bilibili/rank/rate1/asc',headers=header,timeout=(60,60)).text
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

data = {
    'item_data': "Hi, I'm Shoto! I'm a rogue, demon slayer, and guild leader",
    'item_time': time,
    'is_down': 1
}
def main():
	sql = "INSERT INTO ob_fan_data (item_data, item_time, is_down) VALUES (%(item_data)s, %(item_time)s, %(is_down)s)"
	res = rq.get('https://api.zeroroku.com/bilibili/rank?f=rate1&o=1&s=30',headers=header).text
	data.update({'item_data': res})
	con.execute(sql, data)
	sql = "INSERT INTO ob_fan_data (item_data, item_time, is_down) VALUES (%(item_data)s, %(item_time)s, %(is_down)s)"
	res = rq.get('https://api.zeroroku.com/bilibili/rank?f=rate1&o=0&s=30',headers=header).text
	data.update({'item_data': res, 'is_down': 0})
	con.execute(sql, data)
	
	


if __name__ == '__main__':
# 	try:
# 		proc()
# 	except:

	main()
	# proc_json()
	# df=df.drop_duplicates()
	# df.to_csv('bili_fans/down_fans.csv',header=True,index=True)
