#######################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: gatherweathertodb.py
# Description : This is some piece of model to save data to db with
#				good formate for hourlevel and daylevel analysis
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


#################################################################################
# # necessary action to create 2D dictionary
def tree():
    return collections.defaultdict(tree)


#################################################################################
# # get historic weather data
def newweathertocsv():
    api_key = '7579c4fb10268ecb9f10e7ec4ceeb204'

    lat = -37.8136
    lng = 144.9631

    attributes = ["temperature", "humidity","summary","pressure","windSpeed"]

    times = []
    data = {}
    for attr in attributes:
        data[attr] = []
    start = datetime.datetime(2015, 9, 27,tzinfo=pytz.timezone("Australia/Melbourne"))
    for offset in range(0, 30):
        forecast = forecastio.load_forecast(api_key, lat, lng, time=start+datetime.timedelta(offset))
        h = forecast.hourly()
        d = h.data
        for p in d:
            times.append(p.time)
            # print p.time
            # print p.d
            for attr in attributes:
                data[attr].append(p.d[attr])

    df = pd.DataFrame(data,index=times)
    df.to_csv("weather_hist_30_v1.csv")

# newweathertocsv()
# month_names_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#################################################################################
# # format in database
def store_db(db,date,humidity,pressure,summary,temperature,windSpeed):
    storeData = {
                    "time":date,
                    "humidity":humidity,
                    "pressure":pressure,
                    "condition":summary,
                    "temperature":temperature,
                    "windSpeed":windSpeed               
                }
    db.save(storeData)
    pass

#################################################################################
# # save to db as formate above
def csvtodb():
    couch = couchdb.Server('http://127.0.0.1:5984/')
    db = couch['weatherhour']
    with open('weather_hist_30.csv','r') as csvf:
        readline = csv.reader(csvf,delimiter=',',quotechar='|')
        next(csvf, None)
        for row in readline:
            list1 = row[0].split("-")
            list2 = list1[2].split(":")
            list3 = list2[0].split()
            newtimelist = list3[0]+" "+list1[1]+" "+list1[0]+" "+list3[1]+" "+list2[1]+" "+list2[2]
            store_db(db,newtimelist,row[1],row[2],row[3],row[4],row[5])

# csvtodb()

#################################################################################
# # Integrate information for daylevel and hourlevel as a new database
def updatetosummary():
    print "going"
    TARGET_HTTP = '115.146.86.188'
    Weather_HTTP = '127.0.0.1'
    update_HTTP = '127.0.0.1'
    TARGET_DB = 'melbourne_suburb'
    weather_DB = 'weatherhour'
    updatedb = 'coastshop_hour'
    COUCHDB_LINK = 'http://'+TARGET_HTTP+':5984/'+TARGET_DB
    weather_LINK = 'http://'+Weather_HTTP+':5984/'+weather_DB
    updatedb_LINK = 'http://'+update_HTTP+':5984/'

    #################################################################################
    # # to query the view for cities and weather
    db = couchquery.Database(COUCHDB_LINK)
    db_weather = couchquery.Database(weather_LINK)
    # db_update = couchquery.Database(updatedb_LINK)

    #################################################################################
    # # to update summary to the new db
    server = couchdb.Server(updatedb_LINK)
    db_update = server[updatedb]

    #################################################################################
    # # sum each day each city total twitter number 
    rows = db.views.mapreduce.coastshophour(group_level=2)

    NumPerday = tree()
    pnnDistri = tree()

    for row in rows.items():
        if(row[0][1] == 'coast'):
            NumPerday[row[0][0]]['coast'] = row[1][0]
        elif(row[0][1] == 'shop'):
            NumPerday[row[0][0]]['shop'] = row[1][0]
        else:
            NumPerday[row[0][0]]['other'] = row[1][0]


    #################################################################################
    # # calculate the percentage of positive negative netrual for each day each city
    rows = db.views.mapreduce.coastshophour(group_level=3)

    #################################################################################
    # # calculate tweet number and the percentage of positive negative netrual for each 
    # # day each city
    for row in rows.items():
        if row[0][0] in NumPerday:
            pnnDistri[row[0][0]][row[0][1]]['tweets'] = NumPerday[row[0][0]][row[0][1]]
            if row[0][2] == 1:
                pnnDistri[row[0][0]][row[0][1]][1] = float(row[1][0])/NumPerday[row[0][0]][row[0][1]]
            elif row[0][2] == 0:

                pnnDistri[row[0][0]][row[0][1]][0] = float(row[1][0])/NumPerday[row[0][0]][row[0][1]]
            else:
                pnnDistri[row[0][0]][row[0][1]][-1] = float(row[1][0])/NumPerday[row[0][0]][row[0][1]]


    #################################################################################
    # # withdraw weather from weather db and integrate with the emtion percentage 
    dateSuburb = tree()
    rows = db_weather.views.mapreduce.summary()
    for row in rows.items():
        # print row[0][0]
        if row[0][0] in pnnDistri:
            for key,value in pnnDistri[row[0][0]].items():
                smallkey = []
                x={}
                x['region'] = key
                x['date'] = row[0][0]
                x['condition'] = row[0][1]
                x['humidity'] = row[0][2]
                x['pressure'] = row[0][3]
                x['temperature'] = row[0][4]
                x['windSpeed'] =row[0][5]
                # if pnnDistri[row[0][1]][1] is not None:
                x['positive'] = pnnDistri[row[0][0]][key][1]
                # if pnnDistri[row[0][1]][1] is not None:
                x['netrual'] = pnnDistri[row[0][0]][key][0]
                # if pnnDistri[row[0][1]][1] is not None:
                x['negative'] = pnnDistri[row[0][0]][key][-1]
                # if pnnDistri[row[0][1]][1] is not None:
                x['tweets'] = pnnDistri[row[0][0]][key]['tweets']
                smallkey = (row[0][0],key)
                dateSuburb[smallkey] = x
                # print x


            # print x

    #################################################################################
    # # convert to list to rearange the order
    diclist = []            
    for key, value in dateSuburb.iteritems():
        temp = [key,value]
        diclist.append(temp)
    # for key in diclist:
    #   print key[0][0],time.strptime(key[0][0],"%d %b %Y")
    #   timeobject = time.strptime(key[0][0],"%d %b %Y")
    #   print (datetime.datetime(timeobject.tm_year,timeobject.tm_mon,timeobject.tm_mday)-datetime.datetime(1970,1,1)).total_seconds()
    # for key in diclist:
    #   print key[0]
    diclist.sort(key = lambda date:time.strptime(date[0][0],"%d %m %Y"))
    
    # #################################################################################
    # # # update to database
    if len(db_update)>0:
        daterow = []
        for id in db_update:
            doc = db_update[id]
            if('date' in doc.keys()):
                #################################################################################
                # # use this tuple to index and indentify same day same city 
                daterow.append([(doc['date'],doc['region']),id])
        # for key,value in daterow:
        #   print key,value
        # print daterow
        # for id in db_update:
        #   doc = db_update[id]
        #   if('date' in doc.keys()):
        newIndex = [item[0] for item in daterow]

        for key,value in diclist:
            # print key,value
            if(key in newIndex):
                getid = [item[1] for item in daterow if item[0]==key]
                print getid,type(getid[0])
                newid = getid[0]
                doc = db_update[newid]
                if (value['positive'] != doc['positive'] or value['negative'] != doc['negative'] or value['netrual'] != doc['netrual'] or value['tweets'] != doc['tweets']):
                    doc['positive'] = value['positive']
                    doc['negative'] = value['negative']
                    doc['netrual'] = value['netrual']                   
                    db_update[newid] = doc
            if(key not in newIndex):
                print key
                db_update.save(value)
    else:
        for key,value in diclist:
            db_update.save(value)

    # return pnnDistri