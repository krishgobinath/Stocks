
# coding: utf-8

# In[197]:

import pandas_datareader.data as web
import datetime 
from collections import defaultdict
import calendar
import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np
from prettytable import PrettyTable

pyo.offline.init_notebook_mode(connected=True)
month_list =['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', "OCT", 'NOV', 'DEC']


# In[2]:
start = datetime.datetime(2010, 1, 1)
end_b = datetime.datetime.today()
end = datetime.datetime(end_b.year, end_b.month, end_b.day)
#print (end, end_b)
temp_pf="NYSE:ZEN  NASDAQ:INFN  NYSE:FIT  NYSE:TTM  NYSE:ANET  NYSE:SQ  NASDAQ:OSTK  NASDAQ:OKTA  NASDAQ:CAVM  NYSE:ATEN  NASDAQ:BIDU  NASDAQ:ADSK  NASDAQ:KLAC  NYSE:RNG  NASDAQ:AMD  NASDAQ:CHKP  NASDAQ:NVDA  NASDAQ:AMAT  NASDAQ:XLNX  NASDAQ:AMZN  NASDAQ:JD  NASDAQ:FB  NASDAQ:MU  NYSE:BOX  NASDAQ:GOOGL  NYSE:JNPR  NASDAQ:TRMB  NASDAQ:ADBE  NASDAQ:QTNA  NASDAQ:AMBA  NASDAQ:CVLT  NYSE:HPE  NASDAQ:WDC  NYSE:LLL  NYSE:BABA  NASDAQ:NTCT  NASDAQ:ON  NASDAQ:QCOM  NASDAQ:CSCO  NYSE:SNAP  NYSE:ORCL  NASDAQ:NFLX  NASDAQ:MSFT  NASDAQ:NXPI  NASDAQ:NTAP  NASDAQ:MRVL  NYSE:INFY  NYSE:CRM  NYSE:F  NASDAQ:STX  NYSE:CLDR  NASDAQ:TXN  NYSE:TWLO  NASDAQ:PYPL  NASDAQ:WB  NYSE:VMW  NYSE:RHT  NASDAQ:SYMC  NYSE:ACN  NASDAQ:BRCD  NYSE:CIEN  NYSE:MULE  NYSE:TSM  NASDAQ:EBAY  NASDAQ:AAL  NYSE:SSNI  NYSE:YELP  NYSE:CALX  NYSE:GIMO  NASDAQ:FFIV  NASDAQ:COUP  NYSE:GM  NYSE:SAP  NASDAQ:CTXS  NYSE:P  NASDAQ:HIMX  NASDAQ:SPLK  NYSE:TWTR  NASDAQ:NTNX  NASDAQ:AVGO  NYSE:PANW  NASDAQ:AAPL  NASDAQ:FTNT  NASDAQ:GRMN  NYSE:PSTG  NASDAQ:LITE  NASDAQ:GPRO  NYSE:CUDA  NASDAQ:ACIA  NASDAQ:FEYE  NASDAQ:TSLA  NASDAQ:CTSH  NYSE:BB  NASDAQ:AKAM  NASDAQ:MLNX  NYSE:IBM  NASDAQ:GOOG  NASDAQ:AAOI  NASDAQ:COST  NASDAQ:OCLR  NYSE:NPTN  NASDAQ:ADTN  NYSE:CMG  NASDAQ:AQMS  NASDAQ:SLAB  NASDAQ:ROKU"
temp_pf = temp_pf.replace("NASDAQ:", "")
temp_pf = temp_pf.replace("NYSE:", "")
pf = []
for i in temp_pf.split(" "):
    if (i):
        pf.append(str(i))

orginal=pf
dup = list(set(pf))
print (len(orginal), len(dup))
print (pf)


# In[198]:

f = web.DataReader(pf, 'google', start, end)
print (f)


# In[199]:

close_f=f['Close']
volume_f=f['Volume']
tick_by_price = {}
tick_by_met = {}


# In[211]:

def get_max_and_min_of_last_n_days(days=0, weeks=0, months=0, years=0):
    global tick_by_price
    end_b = datetime.datetime.today()
    end = datetime.datetime(end_b.year, end_b.month, end_b.day)
    tot_days = days
    tot_weeks = 0
    if (weeks):
        tot_weeks = weeks
    if (months):        
        tot_weeks = months*4+int(months/2)
    if (years):
        tot_weeks = years*54
    past_week=end-datetime.timedelta(days=tot_days, weeks=tot_weeks)
    print (past_week)
    if (past_week.weekday() == 5):
        offset += 2
        past_week = end-datetime.timedelta(days=tot_days, weeks=tot_weeks)+datetime.timedelta(days=2)
    elif (past_week.weekday() == 6):
        offset += 1
        past_week = end-datetime.timedelta(days=tot_days, weeks=tot_weeks)+datetime.timedelta(days=1)
    else:    
        offset = past_week.weekday()
        past_week = end-datetime.timedelta(days=tot_days,weeks=tot_weeks)+datetime.timedelta(days=-offset)
        
        
    print (past_week, past_week.weekday())
    print (tot_weeks, tot_days)
    dt = ((close_f.index.to_datetime()))
    dtt = dt.to_pydatetime()
    dt_inlist = dtt.tolist()

    while True:
        if past_week in dt_inlist:
            print (dt_inlist.index(past_week), (len(dt_inlist)))    
            break
        else:
            past_week = past_week + datetime.timedelta(days=1)
    start_idx = dt_inlist.index(past_week)
    end_idx = len(dt_inlist)
    
    cclose_f = close_f[start_idx:end_idx+1]
    #print(cclose_f.head())
    for i in range(0, len(pf)):
        tick = pf[i]
        price = np.array((cclose_f[tick].values))
        tick_by_price[tick] = price
        tick_by_met[tick] = (np.min(price), np.max(price), np.std(price), (price[-1]*100)/np.max(price), price[-1])
    temp_infn = np.array((cclose_f['BABA'].values))

    print ((temp_infn))
    #print (np.min(temp_infn), np.max(temp_infn), np.std(temp_infn))
    print (np.min(temp_infn), np.max(temp_infn), np.std(temp_infn), (temp_infn[-1]*100)/np.max(temp_infn), price[-1])
    
        


# In[213]:

get_max_and_min_of_last_n_days(months=3)
t = PrettyTable(['Tick', 'Min', 'Max', 'Standard_deviation', "Percentage", "Current Price"])
for i in range (0, len(pf), 1):
    tick = pf[i]
    minp, maxp, sd, percent, cp = tick_by_met[tick]
    t.add_row([tick, minp, maxp, sd, 100-percent, cp])
print (t)
#print (tick_by_met['TRXC'])
    
    

