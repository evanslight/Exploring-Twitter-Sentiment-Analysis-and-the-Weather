#######################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: hourlevel_timeseries_analysis.py
# Description : This program is to show the scatter matrix and time series
#               plot hourly including coast shop other scenarioes
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


def writeTempTweetcsv():
    TARGET_HTTP = '115.146.86.188'
    TARGET_DB = 'coastshop_hour'
    COUCHDB_LINK = 'http://'+TARGET_HTTP+':5984/'+TARGET_DB

    #################################################################################
    # # to query the view for cities and weather
    db = couchquery.Database(COUCHDB_LINK)

    #################################################################################
    # # calculate the percentage of positive negative netrual for each day each city
    rows = db.views.mapreduce.totalsum(key="coast")
    rows_other = db.views.mapreduce.totalsum(key="other")
    dataframelist = []
    dataframelist_other = []

    #################################################################################
    # # convert date to day month year hour minute second
    for row,other in zip(rows,rows_other):
        # row[0] = time.strptime(row[0], "%d %m %Y %H %M %S")
        row[0] = datetime.datetime.strptime(row[0], "%d %m %Y %H %M %S")
        row[6] =float(row[6])
        row[7] =float(row[7])
        row[8] =float(row[8])
        row[9] =float(row[9])   
        other[0] = datetime.datetime.strptime(other[0], "%d %m %Y %H %M %S")
        other[6] =float(other[6])
        other[7] =float(other[7])
        other[8] =float(other[8])
        other[9] =float(other[9])          
        dataframelist.append(row)
        dataframelist_other.append(other)


    df = pd.DataFrame(dataframelist,columns=['date','positive', 'netrual', 'negative','tweets','condition','humidity','pressure','temperature','windSpeed'])
    indexeddf = df.set_index(['date'])

    df_other = pd.DataFrame(dataframelist_other,columns=['date','positive', 'netrual', 'negative','tweets','condition','humidity','pressure','temperature','windSpeed'])
    indexeddf_other = df_other.set_index(['date'])

    matplotlib.style.use('ggplot')

    #############################################################
    # # withdraw corresponding columns
    dflookup_coast = pd.DataFrame(indexeddf, columns = ['positive', 'netrual', 'negative','tweets','humidity','pressure','temperature','windSpeed'])

    dflookup_other = pd.DataFrame(indexeddf_other, columns = ['positive', 'netrual', 'negative','tweets','humidity','pressure','temperature','windSpeed'])
    # print dflookup_other
    coast_other = dflookup_coast[['positive', 'netrual', 'negative','tweets']].subtract(dflookup_other[['positive', 'netrual', 'negative','tweets']], axis=0)
    coast_other[['humidity','pressure','temperature','windSpeed']] = dflookup_other[['humidity','pressure','temperature','windSpeed']]

    ############################################################
    # # correlation and convariance matrix  
    coast_other.cov().to_csv("coast_other_cov.csv")
    coast_other.corr().to_csv("coast_other_corr.csv")

    coast_other.plot()

    ###########################################################################
    # # scatter matrix
    scatter_matrix(coast_other, alpha=0.2, figsize=(6, 6), diagonal='kde')

    plt.show()
    


writeTempTweetcsv()
