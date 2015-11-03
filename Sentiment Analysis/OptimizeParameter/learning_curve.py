 # -*- coding: utf-8 -*-
#######################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: learning_curve.py
# Description : Draw learing curve for each model  
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

	print "Random Froest"
	target_names = ['Negative', 'Netrual', 'Positive']
	print(classification_report(answer, predict, target_names=target_names))



	answerbi = label_binarize(answer, classes=[0, 1, 2])
	n_classes = answerbi.shape[1]


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


	target_names = ['Negative', 'Netrual', 'Positive']
	print "Logistic Regression"
	print(classification_report(answer, predict, target_names=target_names))



	trainnp = np.asarray(train)
	targetnp = np.asarray(target)
	print targetnp
	X, y = trainnp, targetnp

    ######################################################
    # # ser cross validation for learning curve
	cv = cross_validation.ShuffleSplit(trainnp.shape[0], n_iter=100,test_size=0.2, random_state=0)



	######################################################
	# # draw learning curve for each model 
	
	title = "Learning Curves (Logistic Regression)"
	# estimator = linear_model.LogisticRegression(C=1e5)
	# estimator2 =RandomForestClassifier(n_estimators=110,n_jobs=4)
	# estimator3 = svm.SVC()
	plot_learning_curve(logreg, title, X, y,None, cv=cv, n_jobs=8)
	imgname = "./learningcurve/" +title+'.png'
	fig = plt.gcf()
	fig.set_size_inches(16.5, 12.5)
	fig.savefig(imgname)

	title = "Learning Curves (Random Froest)"
	plot_learning_curve(rf, title, X, y,None, cv=cv, n_jobs=8)

	imgname = "./learningcurve/" +title+'.png'
	fig = plt.gcf()
	fig.set_size_inches(16.5, 12.5)
	fig.savefig(imgname)
	title = "Learning Curves (SVM)"
	plot_learning_curve(clf, title, X, y,None, cv=cv, n_jobs=8)

	imgname = "./learningcurve/" +title+'.png'
	fig = plt.gcf()
	fig.set_size_inches(16.5, 12.5)
	fig.savefig(imgname)

	plt.show()


def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):

    """
    Generate a simple plot of the test and traning learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : integer, cross-validation generator, optional
        If an integer is passed, it is the number of folds (defaults to 3).
        Specific cross-validation objects can be passed, see
        sklearn.cross_validation module for the list of possible objects

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt




if __name__ == '__main__':
    learn()

