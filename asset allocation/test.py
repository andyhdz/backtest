'''
Created on
@author: dangze.huo
'''

import priceseries
import statistics
import numpy
import datetime

dt1 = datetime.date(2015,12,1)

dt1 += datetime.timedelta(1)

for i in range(100):
    print(dt1)
    dt1 += datetime.timedelta(1)
