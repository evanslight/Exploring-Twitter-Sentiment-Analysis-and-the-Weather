#######################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: sentiment_term_frequency.py
# Description : This program is used to build the baseline for sentiment
#                analysis
#######################################################################
import nltk
import re
import csv

tweets_train = []
tweets_test = []
word_features = []
sizeofmylabel = 2613
sizeofsanderlabel = 3036
 



# fileter the text
def filter_tweets_from_traindata(doc):

	#just keep words
	newdoc = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",doc)

	#lower and skip the length lower less 3
	newdoc_filter = [e.lower() for e in newdoc.split() if len(e) >=3]

	return newdoc_filter

# get words in tweets
def get_words_in_tweets(tweets):
	all_words = []

	for (words,sentiment) in tweets:
		all_words.extend(words)

	return all_words

# build the features
def get_words_features(wordlist):

	wordlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	return word_features

# extract the features
def extract_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

# build the classifer for other program invoke
def build_classifier():

	#read our trainData
	with open('trainData.csv','rb') as f:

		myreader = csv.reader(f,delimiter=',')

		#skip the header
		next(myreader, None)

		i = 0
	    #get words in traindata
		for row,value in myreader:

			i += 1

			# set 80% as train set and 20% as test set
			if float(i)/sizeofmylabel <= 0.8:
				tweets_train.append((filter_tweets_from_traindata(row),value))
			else:
				tweets_test.append((filter_tweets_from_traindata(row),value))

			

	#read sanders data
	with open('trainData_Sanders.csv','rU') as f:

		myreader = csv.reader(f)

		#skip the header
		next(myreader, None)


		i = 0

	    #get words in traindata
		for row,value in myreader:
			i += 1

			# set 80% as train set and 20% as test set
			if float(i)/sizeofsanderlabel <= 0.8:
				tweets_train.append((filter_tweets_from_traindata(row),value))
			else:
				tweets_test.append((filter_tweets_from_traindata(row),value))


	#get features from filted tweets
	global word_features
	word_features = get_words_features(get_words_in_tweets(tweets_train))

	#apply the trainning set
	trainning_set = nltk.classify.apply_features(extract_features,tweets_train)


	#set classifier
	classifier = nltk.NaiveBayesClassifier.train(trainning_set)

	return classifier

#interface for prediction
def pre_process(doc):

	return extract_features(filter_tweets_from_traindata(doc))

#get the accuracy for this classifier
def eveluation():

	classifier = build_classifier()

	global word_features
	word_features = get_words_features(get_words_in_tweets(tweets_test))


	test_set = nltk.classify.apply_features(extract_features,tweets_test)

	return nltk.classify.accuracy(classifier,test_set)


if __name__ == '__main__':


	accuracy = eveluation()

	print accuracy

	# text = "i love you"

	# myclass = build_classifier()

	# print myclass.classify(pre_process(text))











		