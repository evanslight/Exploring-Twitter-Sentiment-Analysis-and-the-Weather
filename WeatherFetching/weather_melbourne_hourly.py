#File: weather_melbour_hourly
#Date: 29-Oct-2015
#Author: Hao DUAN<548771> Yu SUN<629341>
#Description: This is a program to Fetch Melbourne hourly weather

import urllib2, urllib, json,os,csv
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import QName
import time
import couchdb

filename = "melbourne_hour.csv"
WEATHER_URL = 'http://weather.yahooapis.com/forecastrss?w=%s'
METRIC_PARAMETER = '&u=c'
# #woeid australia cities
# locationcode=[1103816,1100968,1100661,1105779,1098081,1099805,1102670,1099853,28676628]
locationcode=[1103816]
def find_weather():
	for i in locationcode:
		url = WEATHER_URL % i
		url = url + METRIC_PARAMETER
		xml = ET.parse(urllib.urlopen(url))
		root = xml.getroot()
		ns = "http://xml.weather.yahoo.com/ns/rss/1.0"
		site = root[0][0].text.split(' - ')[1]
		print "Current location is:", site
		# print "Current date is:", root[0][4].text
		# for condition in root.findall('yweather:condition'):
		# 	print "get it"
		# 	print condition.attrib

		body_tag = str(QName(ns,'condition'))
		body = root[0][12].findall(body_tag)
		# print body[0].attrib['date']
		dicweather = body[0].attrib
		# print ' -->',dicweather['date']
		# print ' -->',dicweather['low']
		# print ' -->',dicweather['high']
		# print ' -->',dicweather['text']
		# head = ['date','text','temp','low','location']

		# write_file(filename,
		# 	head,dicweather['date'].split(',')[1].split('AEDT')[0],dicweather['text'],dicweather['temp'],site.split(',')[0])

		store_db(dicweather['date'].split(',')[1].split('AEDT')[0],dicweather['text'],dicweather['temp'])

def store_db(date,weather,temp):
	storeData = {
					"_id":date,
					"weather":weather,
					"temperature":temp
				}
				
	db.save(storeData)
	pass

	


# def write_file(filename,head,date,weather,temp,site):
# 	#check if the file exist
# 	# if not os.path.exists(filename):
# 	# 	with open(filename,'w') as f:
# 	# 		writehead = csv.writer(f,lineterminator='\n')
# 	# 		writehead.writerow(head)

# 	#check the current date wether equal to file date
# 	# new = False
# 	# with open(filename,'r') as f:
# 	# 	readrow = f.readlines()
# 	# 	line = readrow[len(readrow)-1]
# 	# 	for i in range(0,8):
# 	# 		print 1
# 	# 	if line.split(',')[0] <> date:
# 	# 		new = True

# 	#write the new date weather
# 	# if new == True:
# 	with open(filename,'ab') as f:
# 		write = csv.writer(f,lineterminator='\n')
# 		datlist = [date,weather,temp,site]
		# print datlist
		# write.writerow(datlist)	

if __name__ == '__main__':
    while(1):
    	# if not os.path.exists(filename):
    	# 	find_weather()
    	# else:
    	# 	with open(filename,'r') as f:
    	# 		readrow = f.readlines()
    	# 		line = readrow[len(readrow)-1]

    	url = WEATHER_URL % 1103816
    	url = url + METRIC_PARAMETER
    	xml = ET.parse(urllib.urlopen(url))
    	root = xml.getroot()
    	ns = "http://xml.weather.yahoo.com/ns/rss/1.0"
    	site = root[0][0].text.split(' - ')[1]
    	body_tag = str(QName(ns,'condition'))
    	body = root[0][12].findall(body_tag)
    	dicweather = body[0].attrib
    	date = dicweather['date']

    			# if line.split(',')[0] <> date:

    	couch = couchdb.Server('http://127.0.0.1:5984/')
    	db = couch['weather_hourly']

    	find_weather()
    	
        		
        time.sleep(7200)

	







# baseurl = "https://query.yahooapis.com/v1/public/yql?"
# yql_query = "select wind from weather.forecast where woeid=2460286"
# yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
# result = urllib2.urlopen(yql_url).read()
# data = json.loads(result)
# print data['query']['results']
