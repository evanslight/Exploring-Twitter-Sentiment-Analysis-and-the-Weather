#######################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: TweetFecting_9cities.py
# Description : This program is used to fetch tweets located in Australian
#               8 cities
#######################################################################

#import essential libraies
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import re
import sys
import json
import couchdb

# used to sentiment prediction
import Smodel_tweet_getter

# used to judge the location
from shapely.geometry import Polygon
from shapely.geometry import Point




#changed your key here
CONSUMER_KEY = 'uEhP25DfBnk2s3fsVcorHXU2y'
CONSUMER_SECRET = 'hBARKUxJhSacswW0N0rPtEvB4OGWFJllD6FTDCkoJyIMB3xqtV'

ACCESS_TOKEN = '3165109069-yWOdo0QIqFOLNGr3ogweRgAmorwJ73wP6CoVCcy'
ACCESS_TOKEN_SECRET = 'S8sNW8QGLgU1kl3P0rZhnixt19SFRJpwuPwBkUItoMDDW'


#define the Austalia Coordinates
Australia = [112.9,-44.8,159.3,-9.2]

#define the cities of Australia
cities = { 'Melbourne':Polygon(([144.3945,-37.4598], [145.7647, -37.4598],[145.7647,-38.2607],[144.3945,-38.2607],[144.3945,-37.4598])),
           'Canberra':Polygon(([148.8104,-35.1245], [149.3993, -35.1245], [149.3993,-35.5928],[148.8104,-35.5928],[148.8104,-35.1245])),
           'Brisbane':Polygon(([152.4528,-26.7775], [153.5529, -26.7775], [153.5529, -28.0373], [152.4528,-28.0373], [152.4528, -26.7775])),
           'Sydney':Polygon(([150.5022, -33.4246], [151.3426, -33.4246], [151.3426, -34.1692], [150.5022, -34.1692], [150.5022, -33.4246])),
           'Perth':Polygon(([115.4488, -31.4549], [116.4139, -31.4549], [116.4139, -32.4829], [115.4488, -32.4829], [115.4488, -31.4549])),
           'Adelaide':Polygon(([138.3603,-34.5079],[139.0436,-34.5079], [139.0436, -35.4641], [138.3603, -35.4641], [138.3603, -34.5079])),
           'Hobart':Polygon(([147.147807,-42.61712],[147.612863,-42.61712], [147.612863, -43.066664], [147.147807, -43.066664], [147.147807, -42.61712])),
           'Darwin':Polygon(([130.815152, -12.330012], [131.2006, -12.330012], [131.2006, -12.85971], [130.815152,-12.85971], [130.815152, -12.330012]))
          }

cityList = []

model = []


#function to get mentioned user
def getMentioned(mentioned):
    resultList = []
    for eachPerson in mentioned:
        if eachPerson["screen_name"]:
            resultList.append({"Name":eachPerson["screen_name"],"id_str":eachPerson["id_str"]})
            pass
        pass
    return resultList

#function to get Topic
def getTopic(topic):
    resultList = []
    for eachTopic in topic:
        if eachTopic["text"] :
            resultList.append(eachTopic["text"])
            pass
        pass
    return resultList

#function to get uploaded media
def getMedia(media):
    resultList = []
    for eachMedia in media:
        if eachMedia["expanded_url"]:
            resultList.append({"type":eachMedia["type"],"url":eachMedia["expanded_url"],"picture":eachMedia["media_url_https"]})
            pass
        pass
    return resultList

#function to get url
def getUrl(mentionedUrl):
    resultList = []
    for eachUrl in mentionedUrl:
        if eachUrl["expanded_url"]:
            resultList.append(eachUrl["expanded_url"])
            pass
        pass
    return resultList

#judge the cities location
def findCities(point):

    CitiesName = None
    
    for key in cities:
        if point.within(cities[key]):
            CitiesName = key
            break
        pass
    return CitiesName

class StdOutListener(StreamListener):
    def on_data(self, data):
        try:

            item = json.loads(data)

            
            #judge who has been mentioned
            mentionedPerson = None
            if item["entities"]["user_mentions"]:
                mentionedPerson = getMentioned(item["entities"]["user_mentions"])
                pass

            #judge the uploaded media
            uploadedMedia = None
            if "media" in item["entities"]:
                uploadedMedia = getMedia(item["entities"]["media"])
                pass


            #judge the metioned topic
            topic = None
            if item["entities"]["hashtags"]:
                topic = getTopic(item["entities"]["hashtags"])
                pass

            #judge the metioned url
            mentionedUrl = None
            if  item["entities"]["urls"]:
                mentionedUrl = getUrl(item["entities"]["urls"])
                pass

            #integrated the entities of text "media":uploadedMedia
            textEntities = {"mentioned":mentionedPerson,"media":uploadedMedia,"topic":topic,"mentionedUrl":mentionedUrl}

            #judge the geoLocation
            geoInfo = None
            if item["coordinates"]:
                geoInfo = {"type":item["coordinates"]["type"],"locations":item["coordinates"]["coordinates"]}
                pass
            elif item["place"]["bounding_box"]:
                geoInfo = {"type":item["place"]["bounding_box"]["type"],"locations":item["place"]["bounding_box"]["coordinates"]}


            #update Polygon geoInfo into Point
            if geoInfo and geoInfo['type'] == 'Polygon':

                p = Polygon(([geoInfo['locations'][0][0][0],geoInfo['locations'][0][0][1]],
                             [geoInfo['locations'][0][1][0],geoInfo['locations'][0][1][1]],
                             [geoInfo['locations'][0][2][0],geoInfo['locations'][0][2][1]],
                             [geoInfo['locations'][0][3][0],geoInfo['locations'][0][3][1]]))
                pCentre = p.centroid

                #update the geoInfo from Polygon to Point
                geoInfo['type'] = u'Point'
                geoInfo['locations']= [pCentre.x,pCentre.y]

                pass

            #store country name and city name
            country = None
            if "country" in item["place"]:
                country = item["place"]["country"]
                pass

            city = None
            if "full_name" in item["place"]:
                if item["place"]["full_name"].split(',')[0] in cityList:
                    city = item["place"]["full_name"].split(',')[0]

            #if not find city, then use coordinate to judge
            if city is None:
                if geoInfo:
                    p = Point(geoInfo['locations'][0],geoInfo['locations'][1])
                    city = findCities(p)
                    pass
                pass

            
            #define the stored data
            storeData = {   "_id":item["id_str"],
                            "text":item["text"],
                            "textInfo":textEntities,
                            "userName":item["user"]["screen_name"],
                            "userImage":item["user"]["profile_image_url"],
                            "TweetTime":item["created_at"],
                            "geoInfo":geoInfo,
                            "country":country,
                            "city":city
            }

            #get sentiment
            storeData['prediction'] = Smodel_tweet_getter.learn(storeData,model[0],model[1],model[2])


            #store information into couchdb
            if city and storeData['userName'] != 'will_i_ammg' and 'prediction' in storeData:
              db.save(storeData)
              print ('Storing tweet_id %s - %s - %s - %s' %(item["id_str"],city,storeData['prediction'],storeData['geoInfo']['type']))
              pass
            else:
              print ('Fileted tweet_id %s - not store - no cities' %item["id_str"])

            return True

        except BaseException, e:
            
            print 'failed ondata,',str(e)
   

    def on_error(self, status):
        print('status: %s' % status)

if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    for key in cities:
        cityList.append(key)

    print 'The Fecting Tweets on Cities:',cityList

    model = Smodel_tweet_getter.buildmodel()

    #define couchdb you can change the ip and db name here
    couch = couchdb.Server('http://127.0.0.1:5984/')
    db = couch['cities'] 

    stream = Stream(auth, listener)

    stream.filter(locations = Australia,languages=["en"])







