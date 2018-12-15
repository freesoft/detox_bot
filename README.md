# "Detox" toxic chat classifier

## Overview

This project is for my University of Illinois at Urbana-Champaign MCS-DS Fall 2018 CS410 project submission. It is required by UIUC that the project need to be uploaded on public Git repository. After getting grade by UIUC, I'm going to keep working on improving the code.

## Features

* The Detox uses TF-IDF, that enables it to penalize and rewards those frequent/rare words along with frequence of words in docs/message.
* Uses Multinomial Naive Bayes classifier, that enables incremental learning without re-learn from the scratch whenever it has new training set to learn.
* Minimum memory footprint while training. Training data size can be controllable depends on the ysstem. Only 300MB-ish memory required with 10,000 CSV chunksize while training.
* Reuse trained classifer engine and also fitted vectorizer so it runs faster after initial execution.
* The engine supports Out-of-core model fitting, a.k.a incremental training/learning. Thank you for Naive Bayes!!!
* Integerated Twitch Chatbot so Moira can be deployed to any TwitchTV channel and determine if chat is toxic.
* Integrated simple web chat app and TwitchTV chatbot.


## How to Use

### Easy difficulty way : Pre-deployed instance on Heroku

For functionality testing, I've deployed simple webapp as Docker image on (https://detox-uiuc-cs410.herokuapp.com/)[https://detox-uiuc-cs410.herokuapp.com/]
Just open one or two of them, annd try multi chat. See how it works. For any toxic chat that Detox recoginze, the messsage will be displayed in red with "toxic" prefix.


### Normal difficulty way : Runing with Docker image in your local

* Enough memory for the machine for training the model and Docker build/run.
* (Docker)[https://www.docker.com] installed.


### Hard difficulty way : in your local with given test dataset

After Git clone the project in your local machine, simply type

```
python detox_engine.py
```

to train the model before running the test app. The code has sme dependency so you probably need to install a few other python libraries that's specified in requirements.txt. brew, apt-get, macport, pip, anaconda, virtualenv, etc. there are many choices you can install those dependencies.



### With TwitchTV channel

The project comes with tiny TwitchTV chatbot(`chatbot.py`), so you can use it to livefeed the chat log into the Detox.<br/>
Simply type

```
python chatbot.py <username> <client id> <oauth2 acccess token> <channel name>
```
and you'll see that the program is collecting the live chat log from the TwhtchTV channel, and determine if chat is toxic or not.<br/>
It will also create a file with same channel name that Chatbox connected(`<channel name>`) and start logging the message.

Parameter explanation:

* `<username>` : Your username on Twitch. 
* `<client id>` : visit https://glass.twitch.tv/ and login with your own Twitch account. Once you create new app, you'll be able to get Client ID on Dashboard -> App section. <br/>
* `<oauth2 access token>` : visit [here](https://twitchapps.com/tmi/#access_token=flwh72scl6503e6bs2xnwl6g6l5jeu&scope=chat%3Aread+chat%3Aedit+channel%3Amoderate+chat_login&token_type=bearer) and click "Connec with Twitch", and use it for `<oauth2 access token>`.
* `<channel name>` : TwitchTV channel name you'd like to deploy Moira. Use the channel name you can check from web browser's url, which is generally all lowercase regardless of what you can see on twitch user's dashboard.


## FAQ

### I'd like to train the classifier with my own data. What should I do?

If you want to see how it generates classfier and train it, not using pre-existing one, simply delete `classifier.joblib` and `vectorizer.joblib` and re-run the above shell command.

Trainig data and test data files are stored in `data/` directory, so if you wnat to test the engine with your own file, simply replace the file with your own. Make sure you match the CSV file format. <br/>
First line should start with following header title,

```
"id","comment_text" 
```
and from 2nd line you can use your own data. The engine doesn't care much about the value in the "id" part and add whatever chat logs you'd like to test.

Training data file has similar format, but it has additional CSV column that needs to be pre-labeled by human so that it can be used for traning purpose.

## TODO ( later )
* Dockerize it or make it deployable on Heroku with one-click
* Add webapp layer that user can add new training chat log or uploading CSV file
* Better persisent layer than local file for classifier and vectorizer.
* More integration support with other chat ( e.g, YouTube, Mixer, etc ) - at least add interface layer for 3rd party integration

## Resources

* Docker Hub docker image : https://hub.docker.com/r/freesoft/uiuc-cs410-fall2018
 * image pull : `docker pull freesoft/uiuc-cs410-fall2018` ( those latest builds are all failing due to memory size issue that build requires, but updated docker image is ready-to-use )
 