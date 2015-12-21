'''
Created on 

@author: dangze.huo
'''

import priceseries
import numpy
import aautility as au

# generate report of file, each line a file name, report in same folder statistics.txt
# currently data file must have same monthly return data
def fwrite(fo, msg, *vars):
    s = str(msg)
    for v in vars:
        s += str(v)
    fo.write(s)
    
    
def report_statistics( ps_list, file, calccoef = False ):
    
    monthly_return_list = [] # used for corrcoef
    #reporting monthly return mean / monthly return sd / annualized return / annualized risk
    #seperated by \t
    fo_info = open(file, 'w+')
    fwrite(fo_info, "Statistical report\n\n" )
    fwrite(fo_info,len(ps_list), ' assets contained. Starting from ', ps_list[0].start_date,' to ',
                  ps_list[0].end_date,'\n')
    fwrite(fo_info,'mean,sd: mean and standard deviation of monthly returns\n')
    fwrite(fo_info,'a-return,a-sd: annualized return(compounded) and risk(monthly sd*sqrt(12)\n\n')
    fwrite(fo_info,'asset\tmean\tsd\ta-return\ta-sd\n')
    for ps in ps_list:
        fwrite(fo_info,ps.name, '\t', '%.2f'%ps.get_mean(), '\t', '%.2f'%ps.get_sd(), '\t',
                      '%.2f'%ps.get_annualized_return(), '\t', '%.2f'%ps.get_annualized_risk(), '\n' )
        monthly_return_list.append(ps.monthly_return)
    fwrite(fo_info,'\n')
    #reporting correlation coefficients   
    #    asset1    asset2
    #asset1    1    2
    #asset2    1    2
    #
    if calccoef:
        coef = numpy.corrcoef(monthly_return_list)
        for ps in ps_list:
            fwrite(fo_info,'\t',ps.name) # line 1
        fwrite(fo_info,'\n')
        for i in range(len(ps_list)):
            fwrite(fo_info,ps_list[i].name, '\t')
            for j in range(len(ps_list)):
                fwrite(fo_info,'%.2f'%coef[i][j],'\t')
            fwrite(fo_info,'\n')
     
        
    fo_info.close()
    
def generate_report( datalist_file ):
    
    # load asset data
    i = datalist_file.rfind( '/' )
    if i == -1 :
        i = datalist_file.rfind( '\\' ) 
        
    if i == -1 :
        print("datalist_file error" )
        return
    dirstr = datalist_file[ 0:i+1 ]
    
    ps_list = []
    monthly_return_list = [] # used for corrcoef
    
    fo_list = open( datalist_file )
    s = fo_list.read().split()
    
    for i in range(int(len(s)/2)):
        ps = priceseries.PriceSeries( s[2*i] ) # LAN CHOU GU PIAO 
        ps.load_from( dirstr+s[2*i+1] )
        priceseries.report_statistics(ps)
        ps_list.append(ps)
          
    fo_list.close()
    au.report( "Loading completed, price list contains: ", len(ps_list), " entries." )
    
    #reporting monthly return mean / monthly return sd / annualized return / annualized risk
    #seperated by \t
    fo_info = open(dirstr+'statistics.txt', 'w+')
    fwrite(fo_info, "Statistical report\n\n" )
    fwrite(fo_info,len(ps_list), ' assets contained. Starting from ', ps_list[0].start_date,' to ',
                  ps_list[0].end_date,'\n')
    fwrite(fo_info,'mean,sd: mean and standard deviation of monthly returns\n')
    fwrite(fo_info,'a-return,a-sd: annualized return(compounded) and risk(monthly sd*sqrt(12)\n\n')
    fwrite(fo_info,'asset\tmean\tsd\ta-return\ta-sd\n')
    for ps in ps_list:
        fwrite(fo_info,ps.name, '\t', '%.2f'%ps.get_mean(), '\t', '%.2f'%ps.get_sd(), '\t',
                      '%.2f'%ps.get_annualized_return(), '\t', '%.2f'%ps.get_annualized_risk(), '\n' )
        monthly_return_list.append(ps.monthly_return)
    fwrite(fo_info,'\n')
    #reporting correlation coefficients   
    #    asset1    asset2
    #asset1    1    2
    #asset2    1    2
    #
    coef = numpy.corrcoef(monthly_return_list)
    for ps in ps_list:
        fwrite(fo_info,'\t',ps.name) # line 1
    fwrite(fo_info,'\n')
    for i in range(len(ps_list)):
        fwrite(fo_info,ps_list[i].name, '\t')
        for j in range(len(ps_list)):
            fwrite(fo_info,'%.2f'%coef[i][j],'\t')
        fwrite(fo_info,'\n')
        
    fo_info.close()
    
    
if __name__ == '__main__':
    generate_report('C:/data/usdata/namelist.txt')
    pass