#File: weather_9city_db
#Date: 29-Oct-2015
#Author: Hao DUAN<548771> Yu SUN<629341>
#Description: This is a program to Fetch Australian 8 cities daily weather 

import urllib2, urllib, json,os,csv
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import QName
import time
import couchdb

WEATHER_URL = 'http://weather.yahooapis.com/forecastrss?w=%s'
METRIC_PARAMETER = '&u=c'
#woeid australia cities
locationcode=[1103816,1100968,1100661,1105779,1098081,1099805,1102670,1099853,28676628]

def find_weather():

	exits = []
		
	for id in db:
		if id != '_design/mapreduce':
			doc = db[id]
			exits.append((doc['date'],doc['city']))
			pass

	print exits
	
	for i in locationcode:
		url = WEATHER_URL % i
		url = url + METRIC_PARAMETER
		xml = ET.parse(urllib.urlopen(url))
		root = xml.getroot()
		ns = "http://xml.weather.yahoo.com/ns/rss/1.0"
		if i == 28676628:
			site = root[0][0].text.split(' - ')[1].split(' ')[0]
			pass
		else:
			site = root[0][0].text.split(' - ')[1]
		
		print "Current location is:", site
		# print "Current date is:", root[0][4].text
		# for condition in root.findall('yweather:condition'):
		# 	print "get it"
		# 	print condition.attrib

		body_tag = str(QName(ns,'forecast'))
		body = root[0][12].findall(body_tag)
		dicweather = body[0].attrib

		storeData = {
					  'date':dicweather['date'],
					  'city':site.split(',')[0],
					  'text':dicweather['text'],
					  'high':dicweather['high'],
					  'low':dicweather['low']
					}

		if (storeData['date'],storeData['city']) not in exits:
			db.save(storeData)
			pass

	


if __name__ == '__main__':
    while(1):

    		url = WEATHER_URL % 1103816
    		url = url + METRIC_PARAMETER
    		xml = ET.parse(urllib.urlopen(url))
    		root = xml.getroot()
    		ns = "http://xml.weather.yahoo.com/ns/rss/1.0"
    		site = root[0][0].text.split(' - ')[1]
    		body_tag = str(QName(ns,'forecast'))
    		body = root[0][12].findall(body_tag)
    		dicweather = body[0].attrib
    		date = dicweather['date']

    		#define your own address of couchdb and db name
    		couch = couchdb.Server('http://127.0.0.1:5984/')
    		db = couch['weatherdb'] 

    		find_weather()

    		#sleep 1 day
    		time.sleep(72000)
	


