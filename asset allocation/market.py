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
        workbook = xlrd.open_workbook(dirstr+fn)
        datasheet = workbook.sheet_by_index(0)
        for i in range(1, datasheet.nrows):
            row = datasheet.row(i)
            symbol = row[0].value
            #date = xlrd.xldate.xldate_as_datetime(row[1].value, workbook.datemode).date() 
            date = datetime.datetime.strptime(row[1].value, '%Y-%m-%d').date()
            price = row[2].value
            
            if symbol not in market_data:
                market_data[symbol] = {}
                
            market_data[symbol][date] = price
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
    print(_today)
    if _today in market_data[sym]:
        return True
    return False

#today's price of sym
def price(sym):
    return market_data[sym][_today]

def history(sym,date):
    return 150

