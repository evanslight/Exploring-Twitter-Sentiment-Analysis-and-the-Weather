 # -*- coding: utf-8 -*-
#######################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: hourlevel_cluster_mds.py
# Description : This program is to show the cluster for hour data mds
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
    TARGET_DB = 'coastshop_hour'
    COUCHDB_LINK = 'http://'+TARGET_HTTP+':5984/'+TARGET_DB

    #################################################################################
    # # to query the view for cities and weather
    db = couchquery.Database(COUCHDB_LINK)

    #################################################################################
    # # calculate the percentage of positive negative netrual for each day each city
    regionlist = ['coast','shop','other']
    for region in regionlist:
        rows = db.views.mapreduce.total_condi(key=region)
        rows_other = db.views.mapreduce.total_condi(key="other")
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

        ##############################################################################
        # withdraw corresponding data
        df = pd.DataFrame(dataframelist,columns=['date','positive', 'netrual', 'negative','tweets','condition','humidity','pressure','temperature','windSpeed'])
        indexeddf = df.set_index(['date'])

        df_other = pd.DataFrame(dataframelist_other,columns=['date','positive', 'netrual', 'negative','tweets','condition','humidity','pressure','temperature','windSpeed'])
        indexeddf_other = df_other.set_index(['date'])


        twitterinfo = ['positive', 'netrual','negative','tweets']
        weahterinfo = ['condition','humidity','pressure','temperature','windSpeed']

        ##############################################################################
        # set parameters for DBSCAN
        n_neighbors = 10
        n_components = 2
        namelist = "hour_dimention_weahterinfo_"+region

        ##############################################################################
        # draw cluster according to Y and compareY after mds
        Y = manifold.Isomap(n_neighbors, n_components).fit_transform(indexeddf[weahterinfo].values)
        compareY = manifold.Isomap(n_neighbors, n_components).fit_transform(indexeddf[twitterinfo].values)
        drawwDBSCAN(Y,compareY,namelist)



##############################################################################
# # newarray     ： is the 2-d numpy array cluster going to be drawn
# # comparearray ： is the 2-d numpy array cluster going to be compare 
# # cityname     :  is relating to the save document name
def drawwDBSCAN(newarray,comparearray,cityname):
    X = StandardScaler().fit_transform(newarray)
    # print newarray
    # print "#########"
    # print X
    # X = newarray
    ##############################################################################
    # Compute DBSCAN
    db = DBSCAN(eps=0.3, min_samples=10).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(X, labels))

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

    imgname = "./clusterimage/hourcondimention/" +cityname+'.png'
    fig = plt.gcf()
    fig.set_size_inches(16.5, 12.5)
    fig.savefig(imgname)

    ScandARI = drawlableCLuster(comparearray,labels,cityname.split('_')[3])
    print ScandARI

    with open('summary_hour_total_dimention.csv','a') as f:
        write = csv.writer(f)
        # write.writerow(['name','clusters','SC'])
        write.writerow([cityname,n_clusters_,metrics.silhouette_score(X, labels, metric='sqeuclidean')])
        write.writerow(["hour_dimention_twitterinfo"+cityname.split('_')[3],ScandARI[0],ScandARI[1],ScandARI[2]])
    # plt.show()


def drawlableCLuster(yyaxis,twitterlabel,cityname):
    ##############################################################################
    # Compute Affinity Propagation
    X = yyaxis
    db = DBSCAN(eps=0.3, min_samples=10).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(X, labels))
    print("Adjusted Mutual Information: %0.3f"
          % metrics.adjusted_mutual_info_score(twitterlabel, labels))

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

    imgname = "./clusterimage/hourcondimention/" +"hour_dimention_twitterinfo_"+cityname+'.png'
    fig = plt.gcf()
    fig.set_size_inches(16.5, 12.5)
    fig.savefig(imgname)
    # plt.show()
    return [n_clusters_,metrics.silhouette_score(X, labels),metrics.adjusted_mutual_info_score(twitterlabel, labels)]

if __name__ == '__main__':
    writeTempTweetcsv()
