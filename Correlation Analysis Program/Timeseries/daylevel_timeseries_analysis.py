#######################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: daylevel_timeseries_analysis.py
# Description : This program is to show the scatter matrix and time series
#               plot for day data Melbourne or other any cities
#######################################################################

import pandas as pd
import forecastio
import getpass
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import couchquery, collections, couchdb
import time, datetime, pytz, csv
from pandas.tools.plotting import scatter_matrix
from pandas.tools.plotting import autocorrelation_plot
from pandas.tools.plotting import bootstrap_plot
from sklearn import preprocessing
import gatherweathertodb

#################################################################################
# # show the scatter matrix and time series
def writeTempTweetcsv():
    TARGET_HTTP = '115.146.86.188'
    TARGET_DB = 'citysummary'
    COUCHDB_LINK = 'http://'+TARGET_HTTP+':5984/'+TARGET_DB

    #################################################################################
    # # to query the view for cities and weather
    db = couchquery.Database(COUCHDB_LINK)

    #################################################################################
    # # calculate the percentage of positive negative netrual for each day each city
    rows = db.views.mapreduce.emotionTemp(key="Melbourne")
    rows_other = db.views.mapreduce.emotionTemp(key="Sydney")
    dataframelist = []
    dataframelist_other = []

    #################################################################################
    # # convert date to day month year
    for row,other in zip(rows,rows_other):
        # row[0] = time.strptime(row[0], "%d %m %Y %H %M %S")
        row[0] = datetime.datetime.strptime(row[0], "%d %b %Y")
        row[4] =float(row[4])
        row[5] =float(row[5])
 
        other[0] = datetime.datetime.strptime(other[0], "%d %b %Y")
        other[4] =float(other[4])
        other[5] =float(other[5])
          
        dataframelist.append(row)
        dataframelist_other.append(other)


    df = pd.DataFrame(dataframelist,columns=['date','positive', 'netrual', 'negative','high','low','diff','tweets','condition'])
    indexeddf = df.set_index(['date'])

    df_other = pd.DataFrame(dataframelist_other,columns=['date','positive', 'netrual', 'negative','high','low','diff','tweets','condition'])
    indexeddf_other = df_other.set_index(['date'])

    matplotlib.style.use('ggplot')

    # dflookup = pd.DataFrame(indexeddf, columns = ['positive', 'netrual', 'negative','tweets','humidity','pressure','temperature','windSpeed'])
    dflookup_coast = pd.DataFrame(indexeddf, columns = ['positive', 'netrual', 'negative','high','low','diff','tweets'])

    dflookup_other = pd.DataFrame(indexeddf_other, columns = ['positive', 'netrual', 'negative','high','low','diff','tweets'])
    # print dflookup_other
    # coast_other = dflookup_coast[['positive', 'netrual', 'negative','tweets']].subtract(dflookup_other[['positive', 'netrual', 'negative','tweets']], axis=0)
    # coast_other[['high','low','diff']] = dflookup_other[['high','low','diff']]

    ############################################################
    # # correlation and convariance matrix   
    dflookup_coast.cov().to_csv("Sydney_day_cov.csv")
    dflookup_coast.corr().to_csv("Sydney_day_corr.csv")


    ################################################
    # # withdraw corresponding columns
    dflookup_coast_tweet = pd.DataFrame(indexeddf_other, columns = ['positive', 'netrual', 'negative','tweets'])
    dflookup_coast_temp = pd.DataFrame(indexeddf_other, columns = ['positive', 'netrual', 'negative','high','low','diff'])
    dflookup_coast_tweet.plot(secondary_y=['tweets'])
    dflookup_coast_temp.plot(secondary_y=['high','low','diff'])

    ###########################################################################
    # # scatter matrix
    scatter_matrix(dflookup_coast, alpha=0.2, figsize=(6, 6), diagonal='kde')

    plt.show()
    

if __name__ == '__main__':
    #################################################################################
    # # before draw time series build view at that database, name as coasthophour
    writeTempTweetcsv()



