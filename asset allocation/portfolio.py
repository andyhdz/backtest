'''
Created on 
@author: dangze.huo
'''

import aautility
import market

threshold = 5
basepoint = 1000

class Asset():
    def __init__(self, sym):
        self.sym = sym
        
    def check(self):
        print(self.sym)
        return market.check(self.sym)
    
    def price(self):
        return market.price(self.sym)
        

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
        
        self._share = []
        for i in range(self.n):
            ast = assets[i]
            w = weights[i]
            if ast.check() != True:
                print('no asset today: ', ast.sym)
                return
            self._share.append(self._base*w/ast.price())
            
        self.report('Portfolio constructed, MV=', self.value(),' ', len(self._assets),' assets')
    
    def value(self):
        mv = 0
        for i in range(self.n):
            mv += self._assets[i].price()*self._share[i]
        return mv
    
    def check(self):
        for ast in self._assets:
            if ast.check() != True:
                return False
        return True
    
    def rebalance(self):
        mv = self.value()
        print(mv)
        for i in range(self.n):
            if abs(self._assets[i].price()*self._share[i]/mv - self._target_weight[i])>self._threshold:
                #rebalance - selling and buying occurs, OCCCURRRRING 
                self.report('On date: ', market.get_today(),
                            'rebalancing because asset ', self._asset[i].sym, ' exceeded threshold' )
                for j in range(self.n):
                    self._share[j] = mv*self._target_weight[j]/self._assets[j].price()
                #DONE
                return
        print(self.value()) 
        
               