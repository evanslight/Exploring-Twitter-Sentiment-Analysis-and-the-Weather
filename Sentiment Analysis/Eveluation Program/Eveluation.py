#######################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: TweetFecting_9cities.py
# Description : This program is used to ger accuracy of different models
#######################################################################

from pattern.en import sentiment
from numpy import array
import csv
import time
import json
import couchdb
from couchdb.design import ViewDefinition
import sys
from os import path
from sklearn.ensemble import RandomForestClassifier
from numpy import genfromtxt, savetxt
from scipy import interp
# import matplotlib.pyplot as plt
import scipy as sp
from sklearn.metrics import roc_curve, auc, accuracy_score, classification_report
from sklearn.preprocessing import label_binarize
from sklearn import svm
from sklearn import cross_validation
from sklearn import linear_model
from sklearn.tree import DecisionTreeClassifier
from sklearn.multiclass import OneVsRestClassifier
import urllib, cStringIO
import cv2
import numpy as np
from sklearn.svm import SVC
import sentiment_pos


TARGET_HTTP = '127.0.0.1'
TARGET_DB = 'trainset'
COUCHDB_LINK='http://'+TARGET_HTTP+':5984/'
MAIN_PATH = "./Data"
rawtrainfile = 'training_new_neg.txt'
rawtestfile= 'test_new_neg.txt'
trainfile= 'train_real.csv'
testfile = 'test_real.csv'
server = couchdb.Server(COUCHDB_LINK)
db = server[TARGET_DB]

updatedb = server['update1']
#print len(db)
def produceFeature(output):
	with open(path.join(MAIN_PATH,output),'wb') as des:
		writer = csv.writer(des,delimiter=",")


		# get data from couchdb 1300 to train and 1300 to test and write it to file
		

		if(output == 'train_real.csv'):
			i = 0
			for id in db:
				row = []
				doc = db[id]
				if(i <= 1800):
					if ('text' in doc.keys()):
						row.append(doc['label'])

						x=featureCalcu(doc['text'])
						
						row.append(x[0])
						row.append(x[1])
						row.append(x[2])

						#picture posted
						if(doc['textInfo']['media']):
							image_v1 = url_to_image(doc['textInfo']['media'][0]['picture'])
							color = opencvImg(image_v1)
							if(len(color)>0):
								row.append(color[0])
								row.append(color[1])
								row.append(color[2])
								row.append(smileDetect(doc['textInfo']['media'][0]['picture']))
							else:
								row.append(-1)
								row.append(-1)
								row.append(-1)
								row.append(smileDetect(doc['textInfo']['media'][0]['picture']))

						else:
							row.append(x[3])
							row.append(-1)
							row.append(-1)
							row.append(x[4])


						#user image 
						# if(doc['userImage']):
						
						# 	# print doc['textInfo']['media'][0]['picture']
							
						# 	row.append(opencvImg(doc['userImage']))

						# else:
						# 	row.append(x[4])

						writer.writerow(row)
					
				i += 1
		elif(output == 'test_real.csv'):
			i = 0
			for id in db:
				row = []
				doc = db[id]
				if(i > 1800):
					if ('text' in doc.keys()):
						x=featureCalcu(doc['text'])

						row.append(doc['label'])
						row.append(x[0])
						row.append(x[1])
						row.append(x[2])
						
						if(doc['textInfo']['media']):
							image_v1 = url_to_image(doc['textInfo']['media'][0]['picture'])
							color = opencvImg(image_v1)
							if(len(color)>0):
								row.append(color[0])
								row.append(color[1])
								row.append(color[2])
								row.append(smileDetect(doc['textInfo']['media'][0]['picture']))
							else:
								row.append(-1)
								row.append(-1)
								row.append(-1)
								row.append(smileDetect(doc['textInfo']['media'][0]['picture']))
						else:
							row.append(x[3])
							row.append(-1)
							row.append(-1)
							row.append(x[4])


						#user image 
						# if(doc['userImage']):
						
						# 	# print doc['textInfo']['media'][0]['picture']
							
						# 	row.append(opencvImg(doc['userImage']))

						# else:
						# 	row.append(x[4])

						writer.writerow(row)
					
				i += 1




#picture feature return each color	array				
def opencvImg(img):
	# url = "https://pbs.twimg.com/media/CPFihb2VAAABdoj.jpg"
	# Load an color image in grayscale
	# img = cv2.imread('img5.jpg',0)
	# img = url_to_image(url)
	# cv2.imshow('image',img)
	row = []
	if(img is None):
		return row
	size = img.shape[0]*img.shape[1]

	# total = img.sum()
	# print total/size

	# for i in range(0,img.shape[0]):
	# 	print np.trapz(img[0], axis=0)
	b = np.sum(np.sum(img,axis=0),axis=0)[0]/size
	g = np.sum(np.sum(img,axis=0),axis=0)[1]/size
	r = np.sum(np.sum(img,axis=0),axis=0)[2]/size
	sumPix = b + g + r
	row = [b/float(sumPix),g/float(sumPix),sumPix/3]
	return row
# turn url into image file
def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# return the image
	return image



# train set
face_cascade = cv2.CascadeClassifier('haarcascade/face.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade/smile.xml')
# smile detect return 
def smileDetect(url):
    # cap = cv2.VideoCapture(0)
    filename = "1.jpg"
    urllib.urlretrieve(url, filename)
    img = cv2.imread(filename)

    if(img is None):
    	return -1

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # important parameter setting
    smiles = smile_cascade.detectMultiScale(gray,1.8, 12)
    faces = face_cascade.detectMultiScale(gray,scaleFactor = 1.3,minNeighbors = 5, minSize=(100,100))

    # face
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

        # smile
        for smile in smiles:
            x2,y2,a2,b2 = smile[0], smile[1], smile[2], smile[3]
            if ((x2>x) and (y2>y) and (w>a2) and (h>b2)):
                return 2
                # roi_gray = gray[y2:y2+b2, x2:x2+a2]
                # roi_color = img[y2:y2+b2, x2:x2+a2]
                pass
        return 1
    return 0



# return precessed data the sequence is score of sentiment, positive count , negative count
def featureCalcu(text):
	answer = []
	value = sentiment(unicode(text))[0]
	degree = sentiment(unicode(text))[1]
	length = len(text.split())
	#calculate positive term number and negative term number
	i = 0
	pCount = 0
	nCount = 0
	sample_list = sentiment(unicode(text)).assessments
	while(i<len(sample_list)):
		if(sample_list[i][1]>0):
			pCount += 1
		elif(sample_list[i][1]<0):
			nCount += 1
		i+=1

	answer.append(value)

	answer.append(pCount/float(length))
	answer.append(nCount/float(length))
	answer.append(-1)
	answer.append(-1)
	
	return answer

# learnning method and present the accuracy for different models
def learn():

	# produceFeature(trainfile)
	dataset = genfromtxt(open('Data/'+trainfile,'r'), delimiter=',',dtype='f8')[0:]
	target = [x[0] for x in dataset]
	train = [x[1:] for x in dataset]
	# print train[1:10]
	# print target
	# print len(train)

	# produceFeature(testfile)
	test = genfromtxt(open('Data/'+testfile,'r'),delimiter=',',dtype='f8')[0:]
	test_target = [x[1:] for x in test]

	#set random forest learning algorithm
	rf=RandomForestClassifier(n_estimators=110,bootstrap=True, min_samples_leaf=10, min_samples_split=10, criterion='gini', max_features=3, max_depth=3,n_jobs=4)
	rf.fit(train, target)
	# for index, x in enumerate(rf.predict_proba(test)):
	# print rf.predict_proba(test)
	# print rf.predict_proba(test_target)
	predicted_probs = [[index+1,x] for index, x in enumerate(rf.predict(test_target))]

	savetxt('Data/sub.csv',predicted_probs, delimiter=',',fmt='%d,%g',header='ID,prediction',comments='')
	testOutcome = genfromtxt(open('Data/sub.csv','r'), delimiter=',',dtype='f8')[1:]
	predictlist =  [x[1] for x in testOutcome]
	#convert from list to ndarray
	predict = array(predictlist)
	# print predict[1:10]
	testAnswer = genfromtxt(open('Data/'+testfile,'r'), delimiter=',',dtype='f8')[0:]
	answerlist =  [x[0] for x in testAnswer]
	answer = array(answerlist)
	# print answer[1:10]
	# Binarize the output
	# print accuracy_score(predict, answer)
	# fpr, tpr, thresholds = roc_curve(predict, answer, pos_label=1)
	# print auc(fpr, tpr)
	# fpr, tpr, thresholds = roc_curve(predict, answer, pos_label=0)
	# print auc(fpr, tpr)
	# fpr, tpr, thresholds = roc_curve(predict, answer, pos_label=-1)
	# print auc(fpr, tpr)

	print "Random Froest"
	target_names = ['Negative', 'Netrual', 'Positive']
	print(classification_report(answer, predict, target_names=target_names))



	answerbi = label_binarize(answer, classes=[0, 1, 2])
	n_classes = answerbi.shape[1]

	# print answerbi[1:10]

	# print answer

	# aucCurve(answer, predict,n_classes)


	#set svm algorithm
	clf = svm.SVC(kernel='linear', C=1)
	clf.fit(train, target)
	# print clf.predict(test_target)
	predicted_probs = [[index+1,x] for index, x in enumerate(clf.predict(test_target))]

	savetxt('Data/subclf.csv',predicted_probs, delimiter=',',fmt='%d,%g',header='ID,prediction',comments='')
	
	testOutcome = genfromtxt(open('Data/subclf.csv','r'), delimiter=',',dtype='f8')[1:]
	predictlist =  [x[1] for x in testOutcome]
	#convert from list to ndarray
	predict = array(predictlist)
	# print predict[1:10]
	# testAnswer = genfromtxt(open('Data/test_real.csv','r'), delimiter=',',dtype='f8')[0:]
	# answerlist =  [x[0] for x in testAnswer]
	# answer = array(answerlist)
	# # print answer[1:10]
	# # Binarize the output
	# answerbi = label_binarize(answer, classes=['0', '1','-1'])
	# n_classes = answerbi.shape[1]
	# print answerbi[1:10]

	target_names = ['Negative', 'Netrual', 'Positive']
	print "SVM"
	print(classification_report(answer, predict, target_names=target_names))
	# print answer

	# aucCurve(answer, predict,n_classes)


	#set logistice regression algorithm
	logreg = linear_model.LogisticRegression(fit_intercept=True, C=1.0, solver='liblinear', max_iter=100, penalty='l2', dual=False)
	logreg.fit(train, target)
	# print clf.predict(test_target)
	predicted_probs = [[index+1,x] for index, x in enumerate(logreg.predict(test_target))]

	savetxt('Data/sublogistic.csv',predicted_probs, delimiter=',',fmt='%d,%g',header='ID,prediction',comments='')
	
	testOutcome = genfromtxt(open('Data/sublogistic.csv','r'), delimiter=',',dtype='f8')[1:]
	predictlist =  [x[1] for x in testOutcome]
	#convert from list to ndarray
	predict = array(predictlist)
	# print predict[1:10]
	# testAnswer = genfromtxt(open('Data/test_real.csv','r'), delimiter=',',dtype='f8')[0:]
	# answerlist =  [x[0] for x in testAnswer]
	# answer = array(answerlist)
	# # print answer[1:10]
	# # Binarize the output
	# answerbi = label_binarize(answer, classes=[0, 1])
	# n_classes = answerbi.shape[1]
	# print answerbi[1:10]

	# print answer

	target_names = ['Negative', 'Netrual', 'Positive']
	print "Logistic Regression"
	print(classification_report(answer, predict, target_names=target_names))
	# aucCurve(answer, predict,n_classes)





def getFeatureFromDB(doc):
	row = []
	if (('text' in doc.keys()) & ('prediction2' not in doc.keys())):
					
		x = featureCalcu(doc['text'])
		row.append(x[0])
		row.append(x[1])
		row.append(x[2])
		if(doc['textInfo']['media']):
			image_v1 = url_to_image(doc['textInfo']['media'][0]['picture'])
			color = opencvImg(image_v1)
			if(len(color)>0):
				row.append(color[0])
				row.append(color[1])
				row.append(color[2])
				row.append(smileDetect(doc['textInfo']['media'][0]['picture']))
			else:
				row.append(-1)
				row.append(-1)
				row.append(-1)
				row.append(smileDetect(doc['textInfo']['media'][0]['picture']))
		else:
			row.append(x[3])
			row.append(-1)
			row.append(-1)
			row.append(x[4])
		feature = np.asarray(row)
		return feature
	else:
		return row
	
	




#loss function
def llfun(act, pred):
    epsilon = 1e-15
    pred = sp.maximum(epsilon, pred)
    pred = sp.minimum(1-epsilon, pred)
    ll = sum(act*sp.log(pred) + sp.subtract(1,act)*sp.log(sp.subtract(1,pred)))
    ll = ll * -1.0/len(act)
    return ll


def aucCurve(y_test,y_score,n_classes):
	# Compute ROC curve and ROC area for each class
	fpr = dict()
	tpr = dict()
	roc_auc = dict()
	fpr[0], tpr[0], _ = roc_curve(y_test, y_score)
	roc_auc[0] = auc(fpr[0], tpr[0])


	print roc_auc[0]


if __name__ == '__main__':
    learn()

