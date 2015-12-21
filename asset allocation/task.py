'''
Created on 

@author: dangze.huo
'''

import market
import portfolio
from datetime import date, timedelta
from datetime import datetime
import priceseries

#Settings:

#back-testing from to 
start_date = date(2013, 9, 2)
end_date = date(2015, 12, 17)
                              
market_data_list = 'c:/data/backtest/filelist.txt'
syms_list = 'c:/data/backtest/syms.txt' # sym weight
portfolio_daily_price = 'c:/data/backtest/portfolio_daily.txt'
log_file = open( portfolio_daily_price,'w+')
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
        weight.append(float(s[2*i+1])/100.0)
          
    fo_list.close()
    
p_prices = []
p_dates = [] # used for construct a price series 
def log_daily( date, p ):
    log_file.write(str(date)+' '+str('%.2f'%p.value())+'\n')
    p_dates.append(date)
    p_prices.append(p.value())

def statistical_results(  ):
    ps = priceseries.PriceSeries('Portfolio')
    ps.set_data(p_dates,p_prices)
    
    print('Portfolio performance----------Return and Risk: ', ps.get_annualized_return(), '\t', ps.get_annualized_risk())
    

def run():
    market.set_today(start_date)
    p = portfolio.Portfolio(assets,weight)
    if p.check_on_date(end_date) != True:
        print( 'No date on end.')
        return
    
    print('Starting: ', p.report_holding())
    while(market.get_today() <= end_date):
        if p.check() != True:
            market.next_day()
            continue
        if p.rebalance():
            print('On date: ', market.get_today(),' ', p.report_holding())
            
        log_daily(market.get_today(), p)
        #print(p.report_holding())
        
        market.next_day()
        
    print('done.')
    #simple statistics
    print('From ',str(start_date),' to ',str(end_date))
    r = []
    tr = 0.0;
    for i in range(len(assets)):
        r.append(100*(assets[i].price_on_date(end_date)/assets[i].price_on_date(start_date)-1))
        print('Asset ', assets[i].sym, ' simple r: ', r[i])
        tr += r[i]*weight[i]
        
    print('Portfolio: ', 100*(p.value_on_date(end_date)/p.value_on_date(start_date)-1))
    print('Target: ', tr)
                   
    
    
    
if __name__ == '__main__':
    init()
    run()
    statistical_results()