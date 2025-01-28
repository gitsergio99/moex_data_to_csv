import datetime as dt
import time
import requests as rq
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS


def date_req_moex(start_date,end_date):
    dt_req = []
    tm_start = dt.datetime.strptime(start_date,'%Y-%m-%d')
    tm_end = dt.datetime.strptime(end_date,'%Y-%m-%d')
    days_line = tm_end - tm_start
    steps = days_line.days//100
    #print(steps)
    for x in range(steps):
        y=x+1
        print(y)
        if x==0:
            dt_req.append([dt.datetime.strftime(tm_start+dt.timedelta(days=(x*100)),'%Y-%m-%d'),dt.datetime.strftime(tm_start+dt.timedelta(days=(y*100)),'%Y-%m-%d')])
#        elif x==steps-1:
#            dt_req.append([dt.datetime.strftime(tm_start+dt.timedelta(days=(x*100)+1),'%Y-%m-%d'),dt.datetime.strftime(tm_end,'%Y-%m-%d')])
        else:
            dt_req.append([dt.datetime.strftime(tm_start+dt.timedelta(days=(x*100)+1),'%Y-%m-%d'),dt.datetime.strftime(tm_start+dt.timedelta(days=(y*100)),'%Y-%m-%d')])
    dt_req.append([dt.datetime.strftime(tm_start+dt.timedelta(days=(steps*100)+1),'%Y-%m-%d'),dt.datetime.strftime(tm_end,'%Y-%m-%d')])
    return dt_req

def get_table_from_moex(dates,ticket):
    table = []
    for date_s_e in dates:
        print(date_s_e)
        url = f'https://iss.moex.com/iss/history/engines/stock/markets/shares/securities/{ticket}?from={date_s_e[0]}&till={date_s_e[1]}&marketprice_board=1'
        print(url)
        resp = rq.get(url,headers={'User-Agent': UserAgent().chrome})
        bs_res = BS(resp.text,'lxml')
        data_res = bs_res.find_all('row')
        del(data_res[-1])
        for row in data_res:
            table.append([row.get('tradedate'),row.get('open'),row.get('high'),row.get('low'),row.get('close'),row.get('legalcloseprice'),row.get('volume')])
    return table

def creat_csv(table_data,ticket,start_date:str, end_date:str):
    st_d = start_date.replace('-','_')
    e_d = end_date.replace('-','_')
    csv_name =f'{ticket}_{st_d}_to_{e_d}.csv'
    with open(csv_name, 'w') as csv_file:
        csv_file.write('Date,Open,High,Low,Close,Adj Close,Volume'+'\n')
        for row in table_data:
            csv_file.write(','.join(map(str, row)) + '\n')

#st_date ='2023-01-01'
#en_date = '2024-01-18'
#res = date_req_moex(st_date,en_date)
#res1 = get_table_from_moex(res,'LSNG')
#creat_csv(res1,'LSNG',st_date,en_date)
#print(res1)
#print(len(res1))
