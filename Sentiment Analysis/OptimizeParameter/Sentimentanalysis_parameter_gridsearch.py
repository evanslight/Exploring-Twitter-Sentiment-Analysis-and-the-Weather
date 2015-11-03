 # -*- coding: utf-8 -*-
#######################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: Sentimentanalysis_parameter_gridsearch.py
# Description : This program is to find the optimized Logisitc Regression
#				SVM and Random Forest parameters		
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
import scipy as sp
from scipy.stats import randint as sp_randint
import urllib, cStringIO
import cv2
import numpy as np
from sklearn.metrics import roc_curve, auc, accuracy_score, classification_report
from sklearn.preprocessing import label_binarize
from sklearn import svm
from sklearn import cross_validation
from sklearn import linear_model
from sklearn.tree import DecisionTreeClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.learning_curve import learning_curve
from sklearn.datasets import load_digits
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
import matplotlib.pyplot as plt
import matplotlib



TARGET_HTTP = '127.0.0.1'
TARGET_DB = 'traindata'
COUCHDB_LINK='http://'+TARGET_HTTP+':5984/'
MAIN_PATH = "./Data"
# rawtrainfile = 'training_new_neg.txt'
# rawtestfile= 'test_new_neg.txt'
trainfile= 'train_real_2000.csv'
testfile = 'test_real_600.csv'

server = couchdb.Server(COUCHDB_LINK)
db = server[TARGET_DB]


##############################################################################
# # tuned_parameters     ： is parameters to be tuned and is dictionary file
# # model                ： is the sklearn model  
def learn(tuned_parameters,model):

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


	# X, y = digits.data, digits.target
	trainnp = np.asarray(train)
	targetnp = np.asarray(target)


	# turn the data in a (samples, feature) matrix:
	X, y = trainnp, targetnp
	# X = digits.images.reshape((n_samples, -1))
	# y = digits.target

	# Split the dataset in two equal parts
	X_train, X_test, y_train, y_test = train_test_split(
	    X, y, test_size=0.5, random_state=0)



	scores = ['precision', 'recall']

	for score in scores:
	    print("# Tuning hyper-parameters for %s" % score)
	    print()

	    clf = GridSearchCV(model, tuned_parameters, cv=5,
	                       scoring='%s_weighted' % score)
	    clf.fit(X_train, y_train)

	    print("Best parameters set found on development set:")
	    print()
	    print(clf.best_params_)
	    print()
	    print("Grid scores on development set:")
	    print()
	    for params, mean_score, scores in clf.grid_scores_:
	        print("%0.3f (+/-%0.03f) for %r"
	              % (mean_score, scores.std() * 2, params))
	    print()

	    print("Detailed classification report:")
	    print()
	    print("The model is trained on the full development set.")
	    print("The scores are computed on the full evaluation set.")
	    print()
	    y_true, y_pred = y_test, clf.predict(X_test)
	    print(classification_report(y_true, y_pred))
	    print()
	

if __name__ == '__main__':
	x = raw_input("input the model need to tune must be one of rf, lr, svm \n ->> ")
	if(x=="rf"):
		model = RandomForestClassifier(n_estimators=110)
		# Set the parameters by cross-validation
		tuned_parameters = {"max_depth": [3, None],
		             		"max_features": [1, 3, 6],
		             		"min_samples_split": [1, 3, 10],
		             		"min_samples_leaf": [1, 3, 10],
		             		"bootstrap": [True, False],
		             		"criterion": ["gini", "entropy"]}


	elif(x=="svm"):
		model = SVC()
		# Set the parameters by cross-validation
		tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
		                     'C': [1, 10, 100, 1000]},
		                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
	elif(x=="lr"):
		model = linear_model.LogisticRegression()
		# Set the parameters by cross-validation
		tuned_parameters = {"penalty" : ['l2'], 
							"dual" : [False,True], 
							"C" : [1.0,1e5], 
							"fit_intercept" : [True,False],  
							"solver" : ['newton-cg','lbfgs','liblinear'], 
							"max_iter" : [100,200]}
	learn(tuned_parameters,model)