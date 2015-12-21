'''
Created on 2015-12-17

@author: dangze.huo
'''

import datetime
import xlrd
import aautility
import statistics

def report_statistics( ps ):
    #ps = PriceSeries('test');
    #ps.load_from('c:/data/usdata/us_reit.xls')
    ps.report( "name: " + ps.name )
    ps.report( ps.start_date, " ", ps.end_date)
    #ps.report( "daily return mean: " + str( ps.get_mean('daily') ))
    #ps.report( "daily return sd: " + str( ps.get_sd('daily')))
    ps.report( "monthly return mean: " + str( ps.get_mean() ))
    ps.report( "monthly return sd: " + str( ps.get_sd()))
    ps.report( "annualized return: " + str( ps.get_annualized_return()))
    ps.report( "annualized risk: " + str( ps.get_annualized_risk()))
    

class DatePrice(aautility.BaseObj):
    def __init__(self, date, price):
        self.price = price
        self.date = date
        
        
        
class PriceSeries(aautility.BaseObj):
    '''
    classdocs
    '''
    
    #self._series: [ DatePrice ]
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    
    def __init__(self, name):
        self._name = name
        pass
    
    @property
    def name(self):
        return self._name
        
    def set_data(self,dates,prices):
        self._series = []
        for i in range(len(prices)):
            self._series.append(DatePrice(dates[i],prices[i]))
        
        self._fill()
        
    def load_from(self, filename, datatype='dateprice'):
        
        self.report('Loading from file: '+filename)
        
        if(datatype == 'dateprice'):
        #loading from daily data with two columns 
            workbook = xlrd.open_workbook(filename)
            datasheet = workbook.sheet_by_index(0)
            
            #line 1: information
            self._series = []
            #filling daily price series and start/end
            self._start_date = datetime.date(2100,1,1)
            self._end_date = datetime.date(1900,1,1)
            
            for i in range(1, datasheet.nrows):
                row = datasheet.row(i)
                date = xlrd.xldate.xldate_as_datetime(row[0].value, workbook.datemode).date()
                
                if(self._start_date > date):
                    self._start_date = date
                if(self._end_date < date):
                    self._end_date = date
                    
                self._series.append( DatePrice( date, row[1].value ) )
            
            self.report('loading completed. '+str(datasheet.nrows-1)+' rows loaded.')  
            
        #end of load_from if dataprice
        self._fill()
        
    def _fill(self):
        #filling daily return from series
        self._daily_return = []
        for i in range( 1,len( self._series ) ):
            self._daily_return.append( 100*(self._series[i].price/self._series[i-1].price -1) )
            #filling monthly return series based on
        self._monthly_return = []
        last_monthend = self._series[0].price
        for i in range(1,len(self._series)):
            dp = self._series[i]
            ldp = self._series[i-1]
            if( (dp.date.month != ldp.date.month) ): #beginning of new month
                r = 100*( ldp.price/last_monthend -1 )
                self._monthly_return.append(r)
                last_monthend = ldp.price
                    
        #check for last daily/monthly cases for consistency : VERY TRICKRY
        dp = self._series[len(self._series)-1]
        ldp = self._series[len(self._series)-2]
        self._monthly_return.append( 100*(dp.price/last_monthend -1 ) )
        #done checking
            
        #delete the first and last
        del self._monthly_return[0]
        del self._monthly_return[ len(self._monthly_return)-1 ]
            
        #report 
        self.report( "monthly return entries: " + str( len(self._monthly_return ) ))
        
        
    def get_value(self, query_date):
        pass
    
    def get_annualized_return(self):
        product = 1.0;
        for i in range( len( self._monthly_return ) ):
            product *= 1 + self._monthly_return[i]/100
            
        return 100*( product**( 12/len( self._monthly_return ) )-1 )
    
    def get_annualized_risk(self):
        return 12**0.5 * self.get_sd();
    
    def get_mean(self, interval='monthly'):
        
        if( interval == 'monthly' ):
            return statistics.mean( self._monthly_return )
        
        if( interval == 'daily' ):
            return statistics.mean( self._daily_return )
        pass
    
    def get_sd(self, interval='monthly'):
        
        if( interval == 'monthly' ):
            return statistics.stdev( self._monthly_return )
        
        if( interval == 'daily' ):
            return statistics.stdev( self._daily_return )
        pass
    
    @property
    def monthly_return(self):
        return self._monthly_return
    
    @property
    def start_date(self):
        return self._start_date;
    
    @property
    def end_date(self):
        return self._end_date;
    