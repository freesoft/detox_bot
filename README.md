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

Four ways to install and use. From using existing Heroku instance to run it locally as usual Python program. 

### Easy difficulty way : Pre-deployed instance on Heroku

For functionality testing, I've deployed simple webapp as Docker image on (https://uiuc-cs410-detox.herokuapp.com)[https://uiuc-cs410-detox.herokuapp.com]
Just open one or two of them, annd try multi chat. See how it works. For any toxic chat that Detox recoginze, the messsage will be displayed in red with "toxic" prefix. **Recommended** if you only need to test how the classifier works.


### Less-easy difficulty way : Deploy app to your Heroku instance

Press following button and install on your own Heroku instance.<br/>
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy) <br/>
You will need to create a Heroku account to use it.

### Normal difficulty way : Runing with Docker image in your local

* Enough memory for the machine for training the model and Docker build/run.
* (Docker)[https://www.docker.com] installed.


### Hard difficulty way : in your local with given test dataset

After Git clone the project in your local machine, simply type

```
python ./webapp.py
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

## How it's implemented

### Initialization process

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile modified=\&quot;2018-12-16T03:23:29.128Z\&quot; host=\&quot;www.draw.io\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15\&quot; etag=\&quot;Bzuwv_gmwOSZrs7nY9MG\&quot; version=\&quot;9.6.5\&quot; type=\&quot;github\&quot;&gt;&lt;diagram name=\&quot;Page-1\&quot; id=\&quot;74e2e168-ea6b-b213-b513-2b3c1d86103e\&quot;&gt;5VrbcqM4EP0aqnYf4uJm7DzGzmW2amY3VdmZ2X2akkEGVQSihBzb+fptgbhJpOxJmSTjzUMCDTRw+nT3aRHLW6a7O47y5AuLMLVcO9pZ3rXluq49s+GPtOwri+PM3MoScxIpW2t4IM9YGdWF8YZEuOidKBijguR9Y8iyDIeiZ0Ocs23/tDWj/bvmKMaG4SFE1LR+J5FI6tew7fbAJ0ziRN16PlUHVih8jDnbZOp+luuty5/qcIpqX+r8IkER23ZM3o3lLTljotpKd0tMJbg1bNV1ty8cbZ6b40wcc8H20+47eSbLq7u75OtfjrD33uzCnVVunhDd4Po9yqcV+xqh8h2x9GJb3mKbEIEfchTKo1sgBdgSkVLYc2BTucNc4N2LD+o0rw+8wizFgu/hFHWBpwBTjPJqwLdteOaBsiWdyDSUQooSceO6hQU2FDI/g9JhkHAWXUk2wl7GMjwECo4MJh6EpPPO04FXrm0cUyTIU9/9EAzqDveMwI0bxJ1g2oN8bmtIFmzDQ6yu6nLMcORP+q6cmeZKIB5jYbgq49K8+OtD5RihirBgux84i0mGJzmgEFBAb7HisBWLJjrvSHjH6TPemZuMd9yB8AdjEd47TPgOBLkMZvkI04U1vZYWzAk8CeZgZFwkLGYZovet9SSwTftUc2cDsE1N1PyxUPMN1ChDUQkby7eMRxOxE2blgLLwoHZbrG5aa5dtiJI4g22K15K6BdCSZPHncu8asFp06tCKsvARTH06A7h8/49yV+78q468UKWqhD1MliMCd+Iy1ZS/A2UKAEH7zmmKry/f59IevE/LjcrjSQvX9Mx7jO/2QX11j9EdOXoVHLnDBEag/r69+OP6FmzfQKAyDhKXv3tP8YKP1lOOUJodgocUFQUJfy2OO4GryR//8tUsP+hqbCVltjOSEUGgBT1DzykJ2tIdEAaAXXv58E1Og0ggkFcolcTOVkU+JLOA3KIf30Jw9oiXjDLe1rg1oVQz1V0whLCXakKmCoGZ7kodSEkUla1zKNH6qXiCXHPtfq75AxNLk39d2nlj5ZpzRDf5eALOu3xnAeeYtV0pOMERkL9kfcVtG2iJi+ohataHySZ7NIvaB9d3RryOkHxVVEYXeJ4+PI4k8Or7jCrwnP9lAwxs/3UNcKYVVcPR2O1vboSrUwREguF3Wi2Hnmtf82f9EEwD36jPl2/a1i5/KoV+vSFJJ/3stfJRd/TWy3D1ZNGLVLXwFpGneuXty4YKkrEUNCWc+yeSwLn2Au3LzrosK+CaSHlZXQqP0rnaCP1bz1iBr4E8pF/edMaq3+Gce4w+/0/1Zf+jF6v18qY7GjtHXCNYKS4K+b2qFJxZsWY8xaX8ZFb5RYmT3fm2G32MauLxbmOUe8Q6+KF0avT4hT2xA68nyifevN7vjFanFuuu/5FaWnDkoq3haH7I0djpaq6HGGSoE+gzWmF6zwoiCJOJtGJCsLRPDD3ZBMuHcvJgMlvAf3txcyunwyJBuXyUdBfLz/UT9LzheCJH1R/uaZJ0rhXNwDOT1J9NBqZ2PVyny1JzsaMQjGNdptska0wSEvjzWwFpJxe0cPT7+RbWmfZFPXCP1CnuaCEzF1rOTqcYWl5ftjr+o/oBR2MXPnMSpozl1SC8yQShVm+BjEjxHrI0p9DPojNOq3k/Lt6QXvFOo1dgt/1PoSqw7f9jeTf/AQ==&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
<script type="text/javascript" src="https://www.draw.io/js/viewer.min.js"></script>

A few customizations are done here.<br/>

* stopwords.txt modification : original stopwords.txt was from CS410 class' PyMetaPy. However, it turned out the target documents that the project was aiming, which is online chat/in-game chat/etc, include so many slang words that doesn't add much meaning in it or simply abbreviation-ish. 

### How the core engine is integrated

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile modified=\&quot;2018-12-16T03:30:02.177Z\&quot; host=\&quot;www.draw.io\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15\&quot; etag=\&quot;I3UR88yBiWHYTAMac1So\&quot; version=\&quot;9.6.5\&quot; type=\&quot;github\&quot;&gt;&lt;diagram name=\&quot;Page-1\&quot; id=\&quot;74e2e168-ea6b-b213-b513-2b3c1d86103e\&quot;&gt;7Zddb9owFIZ/TaTtYlOIk1Au19B10lRpWtmqXlUmOSTWTBw5hoT9+h0Tm3zB1lZqx0W5wXltn+PzvHYMDonW9bWkRXYjEuCO5ya1Q+aO53nu1MUvrewaZTKZeo2SSpYYrRVu2W8wopmYblgCZW+gEoIrVvTFWOQ5xKqnUSlF1R+2EryftaApjITbmPKxescSldkyXLft+AIszUzqi8B0LGn8K5Vik5t8jkdW+0/TvaY2lhlfZjQRVUciVw6JpBCqaa3rCLiGa7E18z6f6D2sW0KuHjPh+3x5r+48/0c4u5nR7KuMgocPxqst5RvDY1ExFWeLn6hGGVVLXF6zfLWzyLCSQjcxPrqErctMrTkKE2wmtMxAp3TxocqYgrKgsR5e4Q5CbbxuU8oWpIK6I5k6rkGsQckdDrHbzm4eu+lC81x1HLRa1jFvQoxIza5JD7Fbctgw8J4AkoxAVrCMEaBOVhTnxzCcPpeh/1IM/RFDLFwDTKiienKuDzhDhGdH0/eCHs1g+t93ZDCi6Xghx7SXWD6SDFPdXoiaxUztIk7Lkq0YSJzzzsJOQIn6AfKU5fCx0PW+t0FwTd0452cJCfsbnARjS7zZq1oSHrHkBLYVh/qTvt4QBuSJac7jvU1xnyYeCR4JLuQ+hL2F/gIRkt6dOEbYQRQcIWQ1CZwqtu3fpMeomQzfBMtV61DgDg5NMABfio2MwczqXm3/CuQOAikqU1CjQHsTD2U/39fpm69dO4g/OHlDOx7rq++eOMKv5OvFm69dO8JZ347D2/OpvobkpXzFx/YXdTO8/d9Crv4A&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
<script type="text/javascript" src="https://www.draw.io/js/viewer.min.js"></script>

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
 