 # -*- coding: utf-8 -*-
#######################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: daylevel_cluster_pairvariable.py
# Description : This program is to show the cluster for day data variables
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
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from itertools import cycle
from sklearn.preprocessing import StandardScaler
from sklearn import manifold
from sklearn.cluster import DBSCAN


def writeTempTweetcsv():
    TARGET_HTTP = '115.146.86.188'
    TARGET_DB = 'citysummary'
    COUCHDB_LINK = 'http://'+TARGET_HTTP+':5984/'+TARGET_DB

    #################################################################################
    # # to query the view for cities and weather
    db = couchquery.Database(COUCHDB_LINK)

    #################################################################################
    # # calculate the percentage of positive negative netrual for each day each city
    citynamelist = ['Adelaide','Alice Springs','Brisbane','Canberra','Darwin','Hobart','Melbourne','Perth','Sydney']
    for citynameitem in citynamelist:
        rows = db.views.mapreduce.condition_deal(key=citynameitem)
        rows_other = db.views.mapreduce.condition_deal(key="Adelaide")
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

        ##############################################################################
        # withdraw corresponding data
        df = pd.DataFrame(dataframelist,columns=['date','positive', 'netrual', 'negative','high','low','diff','tweets','condition'])
        indexeddf = df.set_index(['date'])

        df_other = pd.DataFrame(dataframelist_other,columns=['date','positive', 'netrual', 'negative','high','low','diff','tweets','condition'])
        indexeddf_other = df_other.set_index(['date'])

        newone = indexeddf.fillna(0)

        ##############################################################################
        # draw each evariable pair cluster
        twitterinfo = ['positive', 'netrual','negative','tweets']
        weahterinfo = ['high','low','diff','condition']
        for axisx in twitterinfo:
            for axisy in weahterinfo:
                namelist = axisx+"_"+axisy+"_"+citynameitem
                print axisx,axisy
                drawwDBSCAN(newone[[axisx,axisy]].values,namelist)




##############################################################################
# # newarray     ： is the 2-d numpy array cluster going to be drawn
# # cityname     :  is relating to the save document name
def drawwDBSCAN(newarray,cityname):
    X = StandardScaler().fit_transform(newarray)
    # print newarray
    # print "#########"
    # print X
    print newarray
    X = newarray
    ##############################################################################
    # Compute DBSCAN
    db = DBSCAN(eps=0.3, min_samples=5).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)
    # print("Silhouette Coefficient: %0.3f"
    #       % metrics.silhouette_score(X, labels))

    ##############################################################################
    # Plot result
    matplotlib.style.use('ggplot')
    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)

    imgname = "./clusterimage/day/" +cityname+'.png'
    fig = plt.gcf()
    fig.set_size_inches(16.5, 12.5)
    fig.savefig(imgname)


    with open('summary_day_cities.csv','a') as f:
        write = csv.writer(f)
        # write.writerow(['name','clusters','SC'])
        if(n_clusters_==0):
            write.writerow([cityname,n_clusters_,-1])
        else:
            write.writerow([cityname,n_clusters_,metrics.silhouette_score(X, labels, metric='sqeuclidean')])

        
        # write.writerow(["hour_dimention_twitterinfo",ScandARI[0],ScandARI[1],ScandARI[2]])
    # plt.show()

if __name__ == '__main__':
    writeTempTweetcsv()


