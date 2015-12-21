'''
Created on 
@author: dangze.huo
'''

import aautility
import market

threshold = 100
basepoint = 1000

class Asset():
    def __init__(self, sym):
        self.sym = sym
        
    def check(self):
        #print(self.sym)
        return market.check(self.sym)
    def check_on_date(self,date):
        return market.check_on_date(self.sym, date)
    
    def price(self):
        return market.price(self.sym)
    def price_on_date(self,date):
        return market.price_on_date(self.sym, date)
        

class Portfolio(aautility.BaseObj):
    '''
    classdocs
    '''
    #portfolio construct, build shares, starting with 1000 point
    def __init__(self, assets, weights):
        self._base = basepoint
        self._threshold = threshold/100
        
        self._assets = assets
        self.n = len(self._assets)
        self._target_weight = weights
        
        self._historical_price = {} #historical market value
        
        self._share = []
        for i in range(self.n):
            ast = assets[i]
            w = weights[i]
            if ast.check() != True:
                print('no asset today: ', ast.sym)
                return
            self._share.append(self._base*w/ast.price())
            
        self.report('Portfolio constructed, MV=', self.value(),' ', len(self._assets),' assets ', 
                    'targetw ', self._target_weight, ' threshold ', self._threshold)
    
    def value(self):
        mv = 0
        for i in range(self.n):
            mv += self._assets[i].price()*self._share[i]
        return mv
    def value_on_date(self,date):
        return self._historical_price[date]
        
    def check(self):
        for ast in self._assets:
            if ast.check() != True:
                return False
        return True
    def check_on_date(self,date):
        for ast in self._assets:
            if ast.check_on_date(date) != True:
                return False
        return True
    
    def rebalance(self):
        mv = self.value()
        self._historical_price[market.get_today()] = mv
        #print(mv)
        for i in range(self.n):
            #print(abs(self._assets[i].price()*self._share[i]/mv - self._target_weight[i]))
            #if i == 0: 
                #print('price ', self._assets[i].price(),' share ', self._share[i],' mv ', mv, ' percent ','%.2f'%(self._assets[i].price()*self._share[i]/mv), ' target ','%.2f'%self._target_weight[i] )
            if abs(self._assets[i].price()*self._share[i]/(mv*self._target_weight[i])-1)>self._threshold:
                #rebalance - selling and buying occurs, OCCCURRRRING 
                self.report('On date: ', market.get_today(),
                            'rebalancing because asset ', self._assets[i].sym, ' exceeded threshold' )
                for j in range(self.n):
                    self._share[j] = mv*self._target_weight[j]/self._assets[j].price()
                #DONE
                return True
        #OR do nothing
        return False
        #print(self.value()) 
        
    def report_holding(self):
        return [ self._share ]
        
        
        
        
        
                   