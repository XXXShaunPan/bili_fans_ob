import pandas as pd
import os
import main_color

fans_type="up" if os.environ["fans_type"] else "down"
date_first=os.environ["date_start"].split(" ")
date_first=date_first[0]+"-"+date_first[1]+"::"+date_first[2]
date_last=""
# (?# os.system(r'md temp\temp_pic'))
df=pd.read_csv(f'bili_fans/{fans_type}_fans.csv',index_col=[0])
mids=df.loc['mid']
error_pic=[]
if not date_last:
    df=df.loc['2021-'+date_first:]
else:
    df=df.loc['2021-'+date_first:'2021-'+date_last]
df.loc['mid']=mids

for i in df.columns:
    if df[i].tolist()[:-1]==[0]*(len(df.index)-1):
        del(df[i])

df.loc['color']=main_color.main(df.loc['mid'].tolist())
df.loc['desc']=[""]*len(df.columns)
df=df.reindex(index=['mid','color','desc']+df.index.tolist()[:-3])
df.to_csv('temp/temp.csv',header=True,index=True)
# os.system("tar -zcvf temp.tar temp/")
print('已获取新的dataFrame文件')
# print("\n")
# print(error_pic)
