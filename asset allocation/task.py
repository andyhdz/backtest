'''
Created on 

@author: dangze.huo
'''

import market
import portfolio
from datetime import date, timedelta
from _datetime import datetime

#Settings:

#back-testing from to 
start_date = date(2013, 3, 5)
end_date = date(2015, 11, 30)

market_data_list = 'c:/data/backtest/filelist.txt'
syms_list = 'c:/data/backtest/syms.txt' # sym weight

#END
assets = []
weight = []

def init():
    market.load_data(market_data_list)
    market.set_today(start_date)
    
    fo_list = open( syms_list )
    s = fo_list.read().split()
    
    for i in range(int(len(s)/2)):
        assets.append( portfolio.Asset(s[2*i]) )
        weight.append(float(s[2*i+1]))
          
    fo_list.close()

def run():
    market.set_today(start_date)
    p = portfolio.Portfolio(assets,weight)
    
    while(market.get_today() <= end_date):
        market.next_day()
    
if __name__ == '__main__':
    init()
    run()