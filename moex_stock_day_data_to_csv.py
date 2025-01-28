# -*- coding: utf-8 -*-
import moex_lib as moex

start_date = '2023-01-01'
end_date = '2024-01-26'
ticket = 'MGNT'

res = moex.date_req_moex(start_date,end_date)
res1 = moex.get_table_from_moex(res,ticket)
moex.creat_csv(res1,ticket,start_date,end_date)