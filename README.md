# Detox ChatBot 

## Overview

This project is for my University of Illinois at Urbana-Champaign MCS-DS Fall 2018 CS410 project submission. It is required by UIUC that the project need to be uploaded on public Git repository. After getting grade by UIUC, I'm going to keep working on improving the code.

[[ TODO ]]

## Features
* Detox Chatbot engine uses TF-IDF for vectorizing and Multinomial Naive Bayes classifier. 
* Minimum memory footprint. ( uses CSV partial loading with default 10,000 chunksize )
* Reuse trained classifer engine and also fitted vectorizer so it runs faster after initial execution.
* Also since those files are stored in disk as file, you can simply copy it and use it whereever you want.
* The engine supports Out-of-core model fitting (a.k.a incremental training/learning) ( thank you for Naive Bayes!!! )
* It has integerated Twitch Chatbot so you can test the engine against any TwitchTV channel. ( don't abuse! )

## Requirement

Python3 along with a few modules (csv, nltk, numpy, pandas, joblib, sklearn)

## How to Use


### in your local with given test dataset
After Git clone the project in your local machine, simply type

```
python3 detox_engine.py
```

to run with existing configuration and trained model.
The program will load test data from the file, and print those toxicity logs in the console.

If you want to see how it generates classfier and train it, not using pre-existing one, simply delete `classifier.joblib` and `vectorizer.joblib` and re-run the above shell command.

Trainig data and test data files are stored in `data/` directory, so if you wnat to test the engine with your own file, simply replace the file with your own. Make sure you match the CSV file format. <br/>
First line should start with following header title,

```
"id","comment_text" 
```
and fron 2nd line you can use your own data. The engine doesn't care much about the value in the "id" part and add whatever chat logs you'd like to test.

Training data file has similar format, but it has additional CSV column that needs to be pre-labeled by human so that it can be used for traning purpose.

### With TwitchTV channel

Since the code has tiny TwitchTV chatbot integrated(`chatbot.py`), you can use this python program to live feed the chat log into the engine.
Simply type

```
python3 chatbot.py Moira <client id> <oauth2 acccess token> <channel name>
```
and you'll see that the program is collecting the live chat log from the TwhtchTV channel, and determine if chat is toxic or not.

## TODO ( later )
* Dockerize it or make it deployable on Heroku with one-click
* Add webapp layer that user can add new training chat log or uploading CSV file
* Better persisent layer than local file for classifier and vectorizer.
* More integration support with other chat ( e.g, YouTube, Mixer, etc ) - at least add interface layer for 3rd party integration

## Resources

[[ TODO ]]