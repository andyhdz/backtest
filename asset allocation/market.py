'''
Created on 

@author: dangze.huo
'''

import aautility
import priceseries
import datetime
import xlrd

_today = datetime.date(2015,12,7)
market_data = {}
market_assets = [] # list of priceseries

def load_data(datalist_file):
    i = datalist_file.rfind( '/' )
    if i == -1 :
        i = datalist_file.rfind( '\\' ) 
        
    if i == -1 :
        print("datalist_file error" )
        return
    dirstr = datalist_file[ 0:i+1 ]
    
    fo_list = open( datalist_file )
    s = fo_list.read().split()
    for fn in s:
        #
        #Each file represents an asset
        #
        workbook = xlrd.open_workbook(dirstr+fn)
        datasheet = workbook.sheet_by_index(0)
        
        d = []
        p = []
        for i in range(1, datasheet.nrows):
            row = datasheet.row(i)
            symbol = row[0].value
            #date = xlrd.xldate.xldate_as_datetime(row[1].value, workbook.datemode).date() 
            date = datetime.datetime.strptime(row[1].value, '%Y-%m-%d').date()
            price = row[2].value
            d.append(date)
            p.append(price)
            
            if symbol not in market_data:
                market_data[symbol] = {}
            market_data[symbol][date] = price
        
        ps = priceseries.PriceSeries(datasheet.row(1)[0].value)
        ps.set_data(d,p)
        market_assets.append(ps)
        
    fo_list.close()
    
    
#today related, dynamic structure 
def next_day():
    global _today
    _today += datetime.timedelta(1)
def set_today(td):
    global _today 
    _today = td
    print(td, ' ', _today )
def get_today():
    return _today

#if asset 'sym' is on today 
def check(sym):
    #print(_today)
    if _today in market_data[sym]:
        return True
    return False
def check_on_date(sym,date):
    if date in market_data[sym]:
        return True
    return False
#today's price of sym
def price(sym):
    #print('checking ',sym, ' on ', str(_today), ' price ', market_data[sym][_today])
    return market_data[sym][_today]

def price_on_date(sym,date):
    #print('checking ',sym, ' on ', str(date), ' price ', market_data[sym][date])
    return market_data[sym][date]

