'''
Author : Wonhee Jung ( wonheej2@illinois.edu, wonhee.jung@gmail.com )
Since : Nov, 2018

UIUC MCS-DS CS410 Fall 2018 Project

Those sample data files are downloaded from Kaggle.
'''
import csv
import os
import os.path
import sys
import time
from builtins import range

import nltk
import numpy as np
import pandas as pd
from joblib import dump, load
from nltk import word_tokenize,sent_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report,confusion_matrix

# includes all the defined constant variables.
import constant

os.environ['OMP_NUM_THREADS'] = '3'

# The class will create two joblib files to store the trained classifier and vectorizer so that it can be reused quickly
# instead of training it from the beginning.
# 
# !!!! IMPORTANT !!!
#
# Which means if you ever chagne any code in __init__ that could affect the way how classifier/vectorizer is going to work,
# then you need to delete two files so that program recrete them. Those two files you need to delete are "classifier.joblib", and "vectorizer.joblib"
# defined in constant.py.
class ToxicityClassifier():
    def __init__(self):

        start_time = time.time()

        self.stopwords = set(w.rstrip() for w in open('stopwords.txt'))
        self.vectorizer = TfidfVectorizer(tokenizer=ToxicityClassifier.tokenizer, max_features=20000, stop_words=self.stopwords, analyzer='word', dtype=np.float32)

        # creating the Multinomial Naive Bayes with Laplacian smoothing.
        self.classifier = MultinomialNB()

        # only fit_transform for the first run, and then just transform the vector so that we don't have a situation
        # that your previous incremental traning and new traning set have different number of features, and it ends up
        # Panda/Scikit-learn complaining about it.
        first_run = True

        # if and only if model doesn't exist in the file, execute this block, means you need to delete the existing model file to re-run this.
        if os.path.exists(constant.CLASSIFIER_FILE) == False:
            print("Can't find existing classifier stored in the file. Creating one...")

            # for df in pd.read_csv(constant.TRAINING_DATA_PATH, delimiter=',', error_bad_lines=True, skipinitialspace=True, chunksize=constant.CVS_CHUNKSIZE, iterator=True):
            df = pd.read_csv(constant.TRAINING_DATA_PATH)
            df = df.replace('\n','', regex=True)
            # The data I got have 6 different categorizaiton, not just toxic or not, so merging it all together as one label
            # as long as there is at least one field marked as '1', those will be considered as toxic.
            # Instead of just getting each feature from dataframe, we can actually reduce the size of dataframe by calling df.pop().
            toxic = \
                df.pop('toxic') | \
                df.pop('severe_toxic') | \
                df.pop('obscene') | \
                df.pop('threat') | \
                df.pop('insult') | \
                df.pop('identity_hate')
            
            # I would try word2vec or other word embedding method if I have more time with the project...
            # but this is how I'm going to solve the issue that # of features between previous and new one is going to have.
            # TODO : change those to word embedding + lookup
            #if first_run == True:
            training = self.vectorizer.fit_transform(df['comment_text'])  
                #first_run = False
            #else:
            #    training = self.vectorizer.transform(df['comment_text'])  

            # if you want to check what's the transformed chat log matrix look like, uncomment below lines.
            #print("looking at the shape of the training set...")
            #print(training.shape)
            #print(training)

            print("Initiating training...")
            train_x, test_x, train_y, test_y = train_test_split(training.toarray(), toxic.values, test_size=0.2)
            self.classifier.fit(train_x, train_y)
                
            print("Completed training. Generating classification result...")
            pred_y = self.classifier.predict(test_x)
            print(classification_report(test_y, pred_y))

            # store the classifier and vectorizer so it can be used later    
            print("Storing classifier and vectorizer into disk...")
            dump(self.classifier, constant.CLASSIFIER_FILE)
            dump(self.vectorizer, constant.VECTORIZER_FILE)
        else:
            print("Found existing classifier and vectorizer stored in the file. Loading...")
            self.classifier = load(constant.CLASSIFIER_FILE)
            self.vectorizer = load(constant.VECTORIZER_FILE)

        # to measure programing execution time
        print("--- time spent for initializing the classifier : %s seconds ---" % (time.time() - start_time))


    # get string value as paraemter and return tokenized array after some data massage, cleansing, etc.
    # returned token array won't have any word with length of one or two
    @staticmethod
    def tokenizer(s):
        wordnet_lemmatizer = WordNetLemmatizer()

        s = s.lower() 
        tokens = nltk.tokenize.word_tokenize(s) 
        tokens = [token for token in tokens if len(token) > 2] # remove words with two characters or less, those are probably pronoun and 
        tokens = [wordnet_lemmatizer.lemmatize(token) for token in tokens] # change the word to base form with NLTK's WordNetLematizer
        return tokens

    # with given parameter s, it returns whether s is toxic or not
    # it is not expecting any arrays, it should be just single string value
    def isToxic(self, s):
        #print("input words:", self.vectorizer.transform( np.array([s])).toarray())
        pred = self.classifier.predict( self.vectorizer.transform( np.array([s])).toarray() )
        #print(pd.DataFrame(self.classifier.predict_log_proba( self.vectorizer.transform( np.array([s])).toarray() ), columns=self.classifier.classes_))
        if pred[0] == 1:
            return True
        else:
            return False

# main function if you need to run it separated, not through chatbot.py.
# The function will load local test CSV file and execute the prediction, instead of getting messages from TwitchTV channel it has deployed.
# With "test/test.csv", the code is going to take anothe 300MB +- to load all the text data and process it.
def main():
    print("Initiating...")

    # below file has smaller set of test data. Enable it instead if you want quicker testing
    test_data_path = "data/test_sample.csv"
    # below file has full set of test data. Try with it if you see more dresult. Beware : it will take some time.
    #test_data_path = "data/test.csv"

    toxicClassifier = ToxicityClassifier()

    # loading chat logs from csv file
    df = pd.read_csv(test_data_path, delimiter=',', error_bad_lines=True, skipinitialspace=True)
    df = df.replace('\n','', regex=True)

    # transform test data's chat log to the existing vecorizer so it can be used for prediction        
    data = toxicClassifier.vectorizer.transform( df['comment_text'] )
    preds = toxicClassifier.classifier.predict( data )

    # enable blow if you want to see what's the prediction for entire dataframe.
    # print("preds")
    # print(preds)

    # print(pd.DataFrame(preds, columns=toxicClassifier.classifier.classes_))
    for i in range(len(preds)):
        if preds[i] == 1:
            print("TOXIC>>> " + df['comment_text'].values[i])            


# just in case if need to run the test locally without TwitchBox working together
if __name__ == "__main__":

    if not sys.version_info[:1] == (3,):
        print(sys.version_info[:1] )
        sys.stderr.write("Python version 3 is required.\n")
        exit(1)

    main()
