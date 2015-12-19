'''
Created on 

@author: dangze.huo
'''

def report( msg, *varlist ):
    rptstr = str(msg)
    for var in varlist:
        rptstr += str(var)
        
    print(rptstr)

class BaseObj():
    
    def report( self, msg, *varlist ):
        
        rptstr = str(msg)
        for var in varlist:
            rptstr += str(var)
        
        print(rptstr)
    
    pass