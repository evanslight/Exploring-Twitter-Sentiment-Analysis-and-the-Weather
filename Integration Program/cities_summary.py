#######################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: melbourne_suburb_summary.py
# Description : This program is used integrated the information for
#               for cities to integrate the weather and emotion
#######################################################################
import couchquery, collections, couchdb
import time, datetime


def main():
	print "going"
	TARGET_HTTP = '115.146.86.188'
	update_HTTP = '127.0.0.1'
	TARGET_DB = 'cities'
	weather_DB = 'weatherdb'
	updatedb = 'citysummary'
	COUCHDB_LINK = 'http://'+TARGET_HTTP+':5984/'+TARGET_DB
	weather_LINK = 'http://'+TARGET_HTTP+':5984/'+weather_DB
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
	# # necessary action to create 2D dictionary
	def tree():
	    return collections.defaultdict(tree)

	#################################################################################
	# # sum each day each city total twitter number 
	rows = db.views.mapreduce.cityDate(group_level=2)
	NumPerday = tree()
	pnnDistri = tree()
	for row in rows.items():
	    NumPerday[row[0][0]][row[0][1]] = row[1][0]
	# print NumPerday

	#################################################################################
	# # calculate the percentage of positive negative netrual for each day each city
	rows = db.views.mapreduce.cityDate(group_level=3)

	for row in rows.items():
		if row[0][0] in NumPerday:
			pnnDistri[row[0][0]][row[0][1]]['tweets'] = NumPerday[row[0][0]][row[0][1]]

			if row[0][2] == 1:

				# pnnDistri[(row[0][0],1)] = [float(row[1][0])/NumPerday[row[0][0]]]
				pnnDistri[row[0][0]][row[0][1]][1] = float(row[1][0])/NumPerday[row[0][0]][row[0][1]]
				# print pnnDistri[(row[0][0],1)]
			elif row[0][2] == 0:

				# pnnDistri[(row[0][0],0)] = [float(row[1][0])/NumPerday[row[0][0]]]
				pnnDistri[row[0][0]][row[0][1]][0] = float(row[1][0])/NumPerday[row[0][0]][row[0][1]]
				# print pnnDistri[(row[0][0],0)]
			else:
				# pnnDistri[(row[0][0],-1)] = [float(row[1][0])/NumPerday[row[0][0]]]
				pnnDistri[row[0][0]][row[0][1]][-1] = float(row[1][0])/NumPerday[row[0][0]][row[0][1]]
				# print pnnDistri[(row[0][0],-1)]

	# print pnnDistri

	#################################################################################
	# # withdraw weather from weather db and integrate with the emtion percentage 
	dateCity = tree()
	rows = db_weather.views.mapreduce.cityDateText()
	for row in rows.items():
		x={}
		if row[0][1] in pnnDistri:
			smallkey = []
			x['city'] = row[0][0]
			x['date'] = row[0][1]
			x['condition'] = row[0][2]
			x['high'] = row[0][3]
			x['low'] = row[0][4]
			if pnnDistri[row[0][1]][1] is not None:
				x['positive'] = pnnDistri[row[0][1]][row[0][0]][1]
			if pnnDistri[row[0][1]][1] is not None:
				x['netrual'] = pnnDistri[row[0][1]][row[0][0]][0]
			if pnnDistri[row[0][1]][1] is not None:
				x['negative'] = pnnDistri[row[0][1]][row[0][0]][-1]
			if pnnDistri[row[0][1]][1] is not None:
				x['tweets'] = pnnDistri[row[0][1]][row[0][0]]['tweets']
			smallkey = (row[0][1],row[0][0])
			dateCity[smallkey] = x
			# print x

	#################################################################################
	# # convert to list to rearange the order
	diclist = []			
	for key, value in dateCity.iteritems():
	    temp = [key,value]
	    diclist.append(temp)
	# for key in diclist:
	# 	print key[0][0],time.strptime(key[0][0],"%d %b %Y")
	# 	timeobject = time.strptime(key[0][0],"%d %b %Y")
	# 	print (datetime.datetime(timeobject.tm_year,timeobject.tm_mon,timeobject.tm_mday)-datetime.datetime(1970,1,1)).total_seconds()
	diclist.sort(key = lambda date:time.strptime(date[0][0],"%d %b %Y"))
	# for key in diclist:
	# 	print key[0]
		
	#################################################################################
	# # update to database
	if len(db_update)>0:
		daterow = []
		for id in db_update:
			doc = db_update[id]
			if('date' in doc.keys()):
				#################################################################################
				# # use this tuple to index and indentify same day same city 
				daterow.append([(doc['date'],doc['city']),id])
		# for key,value in daterow:
		# 	print key,value
		# print daterow
		# for id in db_update:
		# 	doc = db_update[id]
		# 	if('date' in doc.keys()):
		newIndex = [item[0] for item in daterow]

		for key,value in diclist:
			# print key,value
			if(key in newIndex):
				getid = [item[1] for item in daterow if item[0]==key]
				#print getid,type(getid[0])
				newid = getid[0]
				doc = db_update[newid]
				if (value['positive'] != doc['positive'] or value['negative'] != doc['negative'] or value['netrual'] != doc['netrual'] or value['tweets'] != doc['tweets']):
					doc['positive'] = value['positive']
					doc['negative'] = value['negative']
					doc['netrual'] = value['netrual']					
					db_update[newid] = doc
			if(key not in newIndex):
				#print key
				db_update.save(value)
	else:
		for key,value in diclist:
			db_update.save(value)


if __name__ == '__main__':

	#keep running and wait a day
    while(1):
    	main() 		
        time.sleep(72000)



