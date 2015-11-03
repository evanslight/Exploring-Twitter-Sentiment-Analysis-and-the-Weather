#######################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: create_db.py
# Description: this file is used to create db in couchdb and views in db
# due to the tidy code, all the view codes will be putted in one line,
# the detailed of view code can see the pdf document, in this directory
#######################################################################

import couchdb
import couchdb.design


#this function is used to create the db in couchdb
def create_db():
	dbList = ['cities','citysummary','coastshop','melbourne_suburb','weather_hourly','weatherdb']

	for dbname in dbList:

		db = couch.create(dbname)

#this function used to create views in weatherdb
def create_view_in_weatherdb():

	db = couch['weatherdb']

	# view1 for offering weather data to web site
	map_function1 = 'function(doc) {'+'\n' +'var cityName = doc["city"]'+'\n'+'emit(cityName,[doc["date"],doc["high"],doc["low"],doc["text"]]);'+'\n'+'}'
	reduce_function1 = ''
	view1 = couchdb.design.ViewDefinition('mapreduce', 'weathersearch', map_function1, reduce_fun=reduce_function1)
	view1.sync(db)

	# view2 for offering all cities' weather data to integration program
	map_function2 = 'function(doc) {'+'\n'+'var cityName = doc["city"]'+'\n'+'emit([cityName,doc["date"],doc["text"],doc["high"],doc["low"]],null);'+'\n'+'}'
	reduce_function2 = ''
	view2 = couchdb.design.ViewDefinition('mapreduce', 'cityDateText', map_function2, reduce_fun=reduce_function2)
	view2.sync(db)

	#view3 for offering melbourne weather data to the integration program
	map_function3 = 'function(doc) {'+'\n'+'var cityName = doc["city"];'+'\n'+'if(cityName == "Melbourne") {'+'\n'+'emit([cityName,doc["date"],doc["text"],doc["high"],doc["low"]],null);}}'
	reduce_function3 =''
	view3 = couchdb.design.ViewDefinition('mapreduce', 'Melbourne', map_function3, reduce_fun=reduce_function3)
	view3.sync(db)

#function used to create views in cities db
def create_view_in_cities():

	db = couch['cities']

	# this view for offering each cities' daily emotion to integration progam
	map_function1 = 'function(doc) {'+'\n'+'var list = doc.TweetTime.split(" ");'+'\n'+'var a = list[2].split("");'+'\n'+'var b = parseInt(a[0])'+'\n'+'if(b==0){'+'\n'+'var timeday = a[1].concat(" ",list[1]," ",list[5])'+'\n'+'emit([timeday,  doc.city, doc.prediction] , 1);}'+'\n'+'else{'+'\n'+'var timeday = list[2].concat(" ",list[1]," ",list[5])'+'\n'+'emit([timeday,  doc.city, doc.prediction] , 1);'+'\n'+'}'+'\n'+'}'
	reduce_function1 = 'function (key, values, rereduce) {'+'\n'+'if (!rereduce){'+'\n'+'var length = values.length'+'\n'+'return [sum(values), length]'+'\n'+'}else{'+'\n'+'var length = sum(values.map(function(v){return v[1]}))'+'\n'+'var result = sum(values.map(function(v){'+'\n'+'return v[0]'+'\n}))'+'\nreturn [result, length]'+'\n}'+'\n}'
	view1 = couchdb.design.ViewDefinition('mapreduce', 'cityDate', map_function1, reduce_fun=reduce_function1)
	view1.sync(db)

	#this view provided 8 cities geo-location tweets to website
	map_function2 = 'function(doc) {' +'\n'+'var list = doc.TweetTime.split(" ");'+'\n'+'var a = list[2].split("");'+'\n'+'var b = parseInt(a[0])'+'\n'+'if(b==0)'+'\n'+'{'+'\n'+'var timeday = a[1].concat(" ",list[1]," ",list[5])'+'\n'+'emit(timeday, doc.geoInfo.locations);'+'\n}'+'\nelse'+'\n{'+'\n'+'var timeday = list[2].concat(" ",list[1]," ",list[5])'+'\n'+'emit(timeday, doc.geoInfo.locations);'+'\n}'+'\n}'
	reduce_function2 =''
	view2 = couchdb.design.ViewDefinition('mapreduce', 'australia', map_function2, reduce_fun=reduce_function2)
	view2.sync(db)

#function used to create views in melbourne_suburb db
def create_view_in_melbourne():

	db = couch['melbourne_suburb']

	#this view provided melbourne geo-location tweets to website
	map_function1 = 'function(doc) {' +'\n'+'var list = doc.TweetTime.split(" ");'+'\n'+'var a = list[2].split("");'+'\n'+'var b = parseInt(a[0])'+'\n'+'if(b==0)'+'\n'+'{'+'\n'+'var timeday = a[1].concat(" ",list[1]," ",list[5])'+'\n'+'emit(timeday, doc.geoInfo.locations);'+'\n}'+'\nelse'+'\n{'+'\n'+'var timeday = list[2].concat(" ",list[1]," ",list[5])'+'\n'+'emit(timeday, doc.geoInfo.locations);'+'\n}'+'\n}'
	reduce_function1 =''
	view1 = couchdb.design.ViewDefinition('mapreduce', 'heatMap', map_function1, reduce_fun=reduce_function1)
	view1.sync(db)

	#this view for Offering daily emotion on specific areas (coast/shopping mall) to integration program
	map_function2 ='function(doc) {'+'\nvar list = doc.TweetTime.split(" ");'+'\nvar a = list[2].split("");'+'\nvar b = parseInt(a[0]);'+'\nvar myarr = ["Altona","Altona Meadows","Seaholme","Williamstown","Port Melbourne","Newport","Albert Park","St Kilda West","St Kilda","Elwood","Brighton","Middle Park"];'+'\nvar shop = ["Maribyrnong","South Wharf","Melbourne","Malvern East","Essendon Fields"];'	+'\nif(b==0)'	+'\n{'+'\nvar timeday = a[1].concat(" ",list[1]," ",list[5])'+'\nif(myarr.indexOf(doc.suburb) > -1)'+'\n{'+'\nemit([timeday,"coast", doc.prediction], 1);'+'\n}'+'\nelse if(shop.indexOf(doc.suburb) > -1)'+'\n{'+'\nemit([timeday,"shop", doc.prediction], 1);'+'\n}'+'\nelse'+'\n{'+'\nemit([timeday,"other", doc.prediction], 1);'+'\n}}'	+'\nelse'	+'\n{'		+'\nvar timeday = list[2].concat(" ",list[1]," ",list[5])'+'\nif(myarr.indexOf(doc.suburb) > -1)'+'\n{'+'\nemit([timeday,"coast", doc.prediction], 1);'+'\n}'+'\nelse if(shop.indexOf(doc.suburb) > -1)'+'\n{'+'\nemit([timeday,"shop", doc.prediction], 1);'+'\n}'+'\nelse'+'\n{'+'\nemit([timeday,"other", doc.prediction], 1);'+'\n}}}'
	reduce_function2 = 'function (key, values, rereduce) {'+'\n'+'if (!rereduce){'+'\n'+'var length = values.length'+'\n'+'return [sum(values), length]'+'\n'+'}else{'+'\n'+'var length = sum(values.map(function(v){return v[1]}))'+'\n'+'var result = sum(values.map(function(v){'+'\n'+'return v[0]'+'\n}))'+'\nreturn [result, length]'+'\n}'+'\n}'
	view2 = couchdb.design.ViewDefinition('mapreduce', 'coastshop', map_function2, reduce_fun=reduce_function2)
	view2.sync(db)

	#this view for Offering hourly emotion on specific areas (coast/shopping mall) to integration program
	map_function3 = 'function(doc) {'+'\nvar list = doc.TweetTime.split(" ");'+'\nvar a = list[2].split("");'+'\nvar hour = list[3].split(":");'+'\nvar b = parseInt(a[0]);'+'\nvar month_names_short = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]'+'\nvar myarr = ["Altona","Altona Meadows","Seaholme","Williamstown","Port Melbourne","Newport","Albert Park","St Kilda West","St Kilda","Elwood","Brighton","Middle Park"];'+'\nvar shop = ["Maribyrnong","South Wharf","Melbourne","Malvern East","Essendon Fields"];'	+'\nif(b==0)'+'\n{'+'\nvar newmonth = month_names_short.indexOf(list[1])+1;'+'\nvar timeday = list[2].concat(" ",newmonth," ",list[5]," ",hour[0]," ","00"," ","00")'+'\nif(myarr.indexOf(doc.suburb) > -1)'+'\n{'+'\nemit([timeday,"coast", doc.prediction], 1);'+'\n}'+'\nelse if(shop.indexOf(doc.suburb) > -1)'+'\n{'+'\nemit([timeday,"shop", doc.prediction], 1);'+'\n}'+'\nelse'+'\n{'+'\nemit([timeday,"other", doc.prediction], 1);'+'\n}'+'\n}'+'\nelse'+'\n{'+'\nvar newmonth = month_names_short.indexOf(list[1])+1;'+'\nvar timeday = list[2].concat(" ",newmonth," ",list[5]," ",hour[0]," ","00"," ","00")'+'\nif(myarr.indexOf(doc.suburb) > -1)'+'\n{'+'\nemit([timeday,"coast", doc.prediction], 1);'+'\n}'+'\nelse if(shop.indexOf(doc.suburb) > -1)'+'\n{'+'\nemit([timeday,"shop", doc.prediction], 1);'+'\n}'+'\nelse'+'\n{'+'\nemit([timeday,"other", doc.prediction], 1);'+'\n}'+'\n}'+'\n}'
	reduce_function3 = 'function (key, values, rereduce) {'+'\n'+'if (!rereduce){'+'\n'+'var length = values.length'+'\n'+'return [sum(values), length]'+'\n'+'}else{'+'\n'+'var length = sum(values.map(function(v){return v[1]}))'+'\n'+'var result = sum(values.map(function(v){'+'\n'+'return v[0]'+'\n}))'+'\nreturn [result, length]'+'\n}'+'\n}'
	view3 = couchdb.design.ViewDefinition('mapreduce', 'coastshophour', map_function3, reduce_fun=reduce_function3)
	view3.sync(db)

#used to create views in citysummary db
def create_view_in_citysummary():

	db = couch['citysummary']

	#this view for Offering each cities daily emotion to web site
	map_function1 = 'function(doc) {'  +'\nvar cityName = doc["city"]'+'\nemit(cityName,[doc["date"],doc["positive"],doc["netrual"],doc["negative"]]);'+'\n}'
	reduce_function1 = ''
	view1 = couchdb.design.ViewDefinition('mapreduce', 'cityDatePNN', map_function1, reduce_fun=reduce_function1)
	view1.sync(db)

	#this view for Offering 8 cities total negative emotion data on specific weather to website for drawing pie graph
	map_function2 ='function(doc) {'+'\nvar positive;'+'\nvar netrual;'+'\nvar negative;'+'\nvar tweet;'+'\nif(isNaN(doc["positive"]))'+'\n{'+'\n positive = 0;'+'\n}'+'\nelse'+'\n{'+'\npositive = doc["positive"];'+'\n}'+'\nif(isNaN(doc["netrual"]))'+'\n{'+'\n netrual = 0;'+'\n}'+'\nelse'+'\n{'+'\nnetrual = doc["netrual"];'+'\n}'+'\nif(isNaN(doc["negative"]))'+'\n{'+'\n negative = 0;'+'\n}'+'\nelse'+'\n{'+'\nnegative = doc["negative"];'+'\n}'+'\nif(isNaN(doc["tweets"]))'+'\n{'+'\n tweet = 0;'+'\n}'+'\nelse'+'\n{'+'\ntweet = doc["tweets"];'+'\n}'+'\nif(doc["condition"].indexOf("loud")>-1)'+'\n{'+'\ncondition = "Cloud";'+'\n}'+'\nelse if(doc["condition"].indexOf("lear")>-1)'+'\n{'+'\ncondition = "Clear";'+'\n}'+'\nelse if(doc["condition"].indexOf("hower")>-1 || doc["condition"].indexOf("hunder")>-1 || doc["condition"].indexOf("ain")>-1)'+'\n{'+'\ncondition = "Rain";'+'\n}'+'\nelse if(doc["condition"].indexOf("ind")>-1)'+'\n{'+'\ncondition = "Wind";'+'\n}'+'\nelse if(doc["condition"].indexOf("unny")>-1)'+'\n{'+'\ncondition = "Sunny";'+'\n}'+'\nemit(condition,negative);'+'\n}'
	reduce_function2 = 'function (key, values, rereduce) {'+'\nif (!rereduce){'+'\nvar length = values.length'+'\nreturn [sum(values)/length, length]'+'\n}else{'+'\nvar length = sum(values.map(function(v){return v[1]}))'+'\nvar result = sum(values.map(function(v){'+'\nreturn v[0] * (v[1] / length)'+'\n}))'+'\nreturn [result, length]'+'\n}'+'\n}'
	view2 = couchdb.design.ViewDefinition('mapreduce', 'nega_con', map_function2, reduce_fun=reduce_function2)
	view2.sync(db)

	#this view for Offer 8 cities total postive emotion data on specific weather to website for drawing pie graph
	map_function3 ='function(doc) {'+'\nvar positive;'+'\nvar netrual;'+'\nvar negative;'+'\nvar tweet;'+'\nif(isNaN(doc["positive"]))'+'\n{'+'\n positive = 0;'+'\n}'+'\nelse'+'\n{'+'\npositive = doc["positive"];'+'\n}'+'\nif(isNaN(doc["netrual"]))'+'\n{'+'\n netrual = 0;'+'\n}'+'\nelse'+'\n{'+'\nnetrual = doc["netrual"];'+'\n}'+'\nif(isNaN(doc["negative"]))'+'\n{'+'\n negative = 0;'+'\n}'+'\nelse'+'\n{'+'\nnegative = doc["negative"];'+'\n}'+'\nif(isNaN(doc["tweets"]))'+'\n{'+'\n tweet = 0;'+'\n}'+'\nelse'+'\n{'+'\ntweet = doc["tweets"];'+'\n}'+'\nif(doc["condition"].indexOf("loud")>-1)'+'\n{'+'\ncondition = "Cloud";'+'\n}'+'\nelse if(doc["condition"].indexOf("lear")>-1)'+'\n{'+'\ncondition = "Clear";'+'\n}'+'\nelse if(doc["condition"].indexOf("hower")>-1 || doc["condition"].indexOf("hunder")>-1 || doc["condition"].indexOf("ain")>-1)'+'\n{'+'\ncondition = "Rain";'+'\n}'+'\nelse if(doc["condition"].indexOf("ind")>-1)'+'\n{'+'\ncondition = "Wind";'+'\n}'+'\nelse if(doc["condition"].indexOf("unny")>-1)'+'\n{'+'\ncondition = "Sunny";'+'\n}'+'\nemit(condition,positive);'+'\n}'
	reduce_function3 = 'function (key, values, rereduce) {'+'\nif (!rereduce){'+'\nvar length = values.length'+'\nreturn [sum(values)/length, length]'+'\n}else{'+'\nvar length = sum(values.map(function(v){return v[1]}))'+'\nvar result = sum(values.map(function(v){'+'\nreturn v[0] * (v[1] / length)'+'\n}))'+'\nreturn [result, length]'+'\n}'+'\n}'
	view3 = couchdb.design.ViewDefinition('mapreduce', 'posi_con', map_function3, reduce_fun=reduce_function3)
	view3.sync(db)

	#this view for offering total tweets number to website for drawing bar graph
	map_function4 ='function(doc) {'+'\nvar positive;'+'\nvar netrual;'+'\nvar negative;'+'\nvar tweet;'+'\nif(isNaN(doc["positive"]))'+'\n{'+'\n positive = 0;'+'\n}'+'\nelse'+'\n{'+'\npositive = doc["positive"];'+'\n}'+'\nif(isNaN(doc["netrual"]))'+'\n{'+'\n netrual = 0;'+'\n}'+'\nelse'+'\n{'+'\nnetrual = doc["netrual"];'+'\n}'+'\nif(isNaN(doc["negative"]))'+'\n{'+'\n negative = 0;'+'\n}'+'\nelse'+'\n{'+'\nnegative = doc["negative"];'+'\n}'+'\nif(isNaN(doc["tweets"]))'+'\n{'+'\n tweet = 0;'+'\n}'+'\nelse'+'\n{'+'\ntweet = doc["tweets"];'+'\n}'+'\nif(doc["condition"].indexOf("loud")>-1)'+'\n{'+'\ncondition = "Cloud";'+'\n}'+'\nelse if(doc["condition"].indexOf("lear")>-1)'+'\n{'+'\ncondition = "Clear";'+'\n}'+'\nelse if(doc["condition"].indexOf("hower")>-1 || doc["condition"].indexOf("hunder")>-1 || doc["condition"].indexOf("ain")>-1)'+'\n{'+'\ncondition = "Rain";'+'\n}'+'\nelse if(doc["condition"].indexOf("ind")>-1)'+'\n{'+'\ncondition = "Wind";'+'\n}'+'\nelse if(doc["condition"].indexOf("unny")>-1)'+'\n{'+'\ncondition = "Sunny";'+'\n}'+'\nemit(condition,tweet);'+'\n}'
	reduce_function4 = 'function (key, values, rereduce) {'+'\nif (!rereduce){'+'\nvar length = values.length'+'\nreturn [sum(values)/length, length]'+'\n}else{'+'\nvar length = sum(values.map(function(v){return v[1]}))'+'\nvar result = sum(values.map(function(v){'+'\nreturn v[0] * (v[1] / length)'+'\n}))'+'\nreturn [result, length]'+'\n}'+'\n}'
	view4 = couchdb.design.ViewDefinition('mapreduce', 'tweet_con', map_function4, reduce_fun=reduce_function4)
	view4.sync(db)

	map_function5 = 'function(doc) {'+'\nvar cityName = doc["city"]'+'\nvar positive;'+'\nvar netrual;'+'\nvar negative;'+'\nvar tweet;'+'\nvar diff = parseFloat(doc["high"])-parseFloat(doc["low"]);'+'\nif(isNaN(doc["positive"]))'+'\n{'+'\npositive = 0;'+'\n}'+'\nelse'+'\n{'+'\npositive = doc["positive"];'+'\n}'+'\nif(isNaN(doc["netrual"]))'+'\n{'+'\nnetrual = 0;'+'\n}'+'\nelse'+'\n{'+'\nnetrual = doc["netrual"];'+'\n}'+'\nif(isNaN(doc["negative"]))'+'\n{'+'\nnegative = 0;'+'\n}'+'\nelse'+'\n{'+'\nnegative = doc["negative"];'+'\n}'+'\nif(isNaN(doc["tweets"]))'+'\n{'+'\ntweet = 0;'+'\n}'+'\nelse'+'\n{'+'\ntweet = doc["tweets"];'+'\n}'+'\nif(doc["condition"].indexOf("loud")>-1)'+'\n{'+'\ncondition = "Cloud";'+'\n}'+'\nelse if(doc["condition"].indexOf("lear")>-1)'+'\n{'+'\ncondition = "Clear";'+'\n}'+'\nelse if(doc["condition"].indexOf("hower")>-1 || doc["condition"].indexOf("hunder")>-1 || doc["condition"].indexOf("ain")>-1)'+'\n{'+'\ncondition = "Rain";'+'\n}'+'\nelse if(doc["condition"].indexOf("ind")>-1)'+'\n{'+'\ncondition = "Wind";'+'\n}'+'\nelse if(doc["condition"].indexOf("unny")>-1)'+'\n{'+'\ncondition = "Sunny";'+'\n}'+'\nemit(cityName,[doc["date"],positive,netrual,negative,doc["high"],doc["low"],diff,doc["tweets"],condition]);'+'\n}'
	reduce_function5=''
	view5 = couchdb.design.ViewDefinition('mapreduce', 'emotionTemp', map_function5, reduce_fun=reduce_function5)
	view5.sync(db)

# used to create view in coastshop
def create_view_in_coastshop():

	db = couch['coastshop']

	map_function1 ='function(doc) {'+'\nvar cityName = doc["region"];'+'\nvar positive;'+'\nvar netrual;'+'\nvar negative;'+'\nvar tweet;'+'\nvar diff = parseFloat(doc["high"])-parseFloat(doc["low"]);'+'\nif(isNaN(doc["positive"]))'+'\n{'+'\npositive = 0;'+'\n}'+'\nelse'+'\n{'+'\npositive = doc["positive"];'+'\n}'+'\nif(isNaN(doc["netrual"]))'+'\n{'+'\nnetrual = 0;'+'\n}'+'\nelse'+'\n{'+'\nnetrual = doc["netrual"];'+'\n}'+'\nif(isNaN(doc["negative"]))'+'\n{'+'\nnegative = 0;'+'\n}'+'\nelse'+'\n{'+'\nnegative = doc["negative"];'+'\n}'+'\nif(isNaN(doc["tweets"]))'+'\n{'+'\ntweet = 0;'+'\n}'+'\nelse'+'\n{'+'\ntweet = doc["tweets"];'+'\n}'+'\nemit(cityName,[doc["date"],positive,netrual,negative,doc["high"],doc["low"],diff,doc["tweets"],doc["condition"]]);'+'\n}' 
	reduce_function1 = ''
	view1 = couchdb.design.ViewDefinition('mapreduce', 'region', map_function1, reduce_fun=reduce_function1)
	view1.sync(db)

	#this view for Offering Melbourne suburbs total negative emotion data on specific weather to website for drawing pie graph
	map_function2 ='function(doc) {'+'\nvar positive;'+'\nvar netrual;'+'\nvar negative;'+'\nvar tweet;'+'\nif(isNaN(doc["positive"]))'+'\n{'+'\n positive = 0;'+'\n}'+'\nelse'+'\n{'+'\npositive = doc["positive"];'+'\n}'+'\nif(isNaN(doc["netrual"]))'+'\n{'+'\n netrual = 0;'+'\n}'+'\nelse'+'\n{'+'\nnetrual = doc["netrual"];'+'\n}'+'\nif(isNaN(doc["negative"]))'+'\n{'+'\n negative = 0;'+'\n}'+'\nelse'+'\n{'+'\nnegative = doc["negative"];'+'\n}'+'\nif(isNaN(doc["tweets"]))'+'\n{'+'\n tweet = 0;'+'\n}'+'\nelse'+'\n{'+'\ntweet = doc["tweets"];'+'\n}'+'\nif(doc["condition"].indexOf("loud")>-1)'+'\n{'+'\ncondition = "Cloud";'+'\n}'+'\nelse if(doc["condition"].indexOf("lear")>-1)'+'\n{'+'\ncondition = "Clear";'+'\n}'+'\nelse if(doc["condition"].indexOf("hower")>-1 || doc["condition"].indexOf("hunder")>-1 || doc["condition"].indexOf("ain")>-1)'+'\n{'+'\ncondition = "Rain";'+'\n}'+'\nelse if(doc["condition"].indexOf("ind")>-1)'+'\n{'+'\ncondition = "Wind";'+'\n}'+'\nelse if(doc["condition"].indexOf("unny")>-1)'+'\n{'+'\ncondition = "Sunny";'+'\n}'+'\nemit(condition,negative);'+'\n}'
	reduce_function2 = 'function (key, values, rereduce) {'+'\nif (!rereduce){'+'\nvar length = values.length'+'\nreturn [sum(values)/length, length]'+'\n}else{'+'\nvar length = sum(values.map(function(v){return v[1]}))'+'\nvar result = sum(values.map(function(v){'+'\nreturn v[0] * (v[1] / length)'+'\n}))'+'\nreturn [result, length]'+'\n}'+'\n}'
	view2 = couchdb.design.ViewDefinition('mapreduce', 'nega_aver', map_function2, reduce_fun=reduce_function2)
	view2.sync(db)

	#this view for Offering Melbourne suburbs total postive emotion data on specific weather to website for drawing pie graph
	map_function3 ='function(doc) {'+'\nvar positive;'+'\nvar netrual;'+'\nvar negative;'+'\nvar tweet;'+'\nif(isNaN(doc["positive"]))'+'\n{'+'\n positive = 0;'+'\n}'+'\nelse'+'\n{'+'\npositive = doc["positive"];'+'\n}'+'\nif(isNaN(doc["netrual"]))'+'\n{'+'\n netrual = 0;'+'\n}'+'\nelse'+'\n{'+'\nnetrual = doc["netrual"];'+'\n}'+'\nif(isNaN(doc["negative"]))'+'\n{'+'\n negative = 0;'+'\n}'+'\nelse'+'\n{'+'\nnegative = doc["negative"];'+'\n}'+'\nif(isNaN(doc["tweets"]))'+'\n{'+'\n tweet = 0;'+'\n}'+'\nelse'+'\n{'+'\ntweet = doc["tweets"];'+'\n}'+'\nif(doc["condition"].indexOf("loud")>-1)'+'\n{'+'\ncondition = "Cloud";'+'\n}'+'\nelse if(doc["condition"].indexOf("lear")>-1)'+'\n{'+'\ncondition = "Clear";'+'\n}'+'\nelse if(doc["condition"].indexOf("hower")>-1 || doc["condition"].indexOf("hunder")>-1 || doc["condition"].indexOf("ain")>-1)'+'\n{'+'\ncondition = "Rain";'+'\n}'+'\nelse if(doc["condition"].indexOf("ind")>-1)'+'\n{'+'\ncondition = "Wind";'+'\n}'+'\nelse if(doc["condition"].indexOf("unny")>-1)'+'\n{'+'\ncondition = "Sunny";'+'\n}'+'\nemit(condition,positive);'+'\n}'
	reduce_function3 = 'function (key, values, rereduce) {'+'\nif (!rereduce){'+'\nvar length = values.length'+'\nreturn [sum(values)/length, length]'+'\n}else{'+'\nvar length = sum(values.map(function(v){return v[1]}))'+'\nvar result = sum(values.map(function(v){'+'\nreturn v[0] * (v[1] / length)'+'\n}))'+'\nreturn [result, length]'+'\n}'+'\n}'
	view3 = couchdb.design.ViewDefinition('mapreduce', 'posi_aver', map_function3, reduce_fun=reduce_function3)
	view3.sync(db)

	#this view for offering melbourne suburbs total tweets number to website for drawing bar graph
	map_function4 ='function(doc) {'+'\nvar positive;'+'\nvar netrual;'+'\nvar negative;'+'\nvar tweet;'+'\nif(isNaN(doc["positive"]))'+'\n{'+'\n positive = 0;'+'\n}'+'\nelse'+'\n{'+'\npositive = doc["positive"];'+'\n}'+'\nif(isNaN(doc["netrual"]))'+'\n{'+'\n netrual = 0;'+'\n}'+'\nelse'+'\n{'+'\nnetrual = doc["netrual"];'+'\n}'+'\nif(isNaN(doc["negative"]))'+'\n{'+'\n negative = 0;'+'\n}'+'\nelse'+'\n{'+'\nnegative = doc["negative"];'+'\n}'+'\nif(isNaN(doc["tweets"]))'+'\n{'+'\n tweet = 0;'+'\n}'+'\nelse'+'\n{'+'\ntweet = doc["tweets"];'+'\n}'+'\nif(doc["condition"].indexOf("loud")>-1)'+'\n{'+'\ncondition = "Cloud";'+'\n}'+'\nelse if(doc["condition"].indexOf("lear")>-1)'+'\n{'+'\ncondition = "Clear";'+'\n}'+'\nelse if(doc["condition"].indexOf("hower")>-1 || doc["condition"].indexOf("hunder")>-1 || doc["condition"].indexOf("ain")>-1)'+'\n{'+'\ncondition = "Rain";'+'\n}'+'\nelse if(doc["condition"].indexOf("ind")>-1)'+'\n{'+'\ncondition = "Wind";'+'\n}'+'\nelse if(doc["condition"].indexOf("unny")>-1)'+'\n{'+'\ncondition = "Sunny";'+'\n}'+'\nemit(condition,tweet);'+'\n}'
	reduce_function4 = 'function (key, values, rereduce) {'+'\nif (!rereduce){'+'\nvar length = values.length'+'\nreturn [sum(values)/length, length]'+'\n}else{'+'\nvar length = sum(values.map(function(v){return v[1]}))'+'\nvar result = sum(values.map(function(v){'+'\nreturn v[0] * (v[1] / length)'+'\n}))'+'\nreturn [result, length]'+'\n}'+'\n}'
	view4 = couchdb.design.ViewDefinition('mapreduce', 'tweet_average', map_function4, reduce_fun=reduce_function4)
	view4.sync(db)

if __name__ == '__main__':

	#define your couch db location here
	couch = couchdb.Server('http://127.0.0.1:5984')

	#create the db
	create_db()

	#create views in weather db
	create_view_in_weatherdb()

	#create views in 8 cities db
	create_view_in_cities()

	#create views in melbourne_suburb db
	create_view_in_melbourne()

	#create views in citysummary db
	create_view_in_citysummary()

	#create views in coastshop db
	create_view_in_coastshop()

	print "The couchdb is already to use!"
