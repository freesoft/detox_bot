FROM ubuntu:18.04
MAINTAINER Wonhee Jung "wonheej2@illinois.edu"
RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3.6 \
    python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install -U nltk
RUN python3 -m nltk.downloader popular
RUN pip3 install -U numpy
RUN pip3 install -r requirements.txt
RUN python3 detox_engine.py
ENTRYPOINT ["python3"]
CMD ["webapp.py"]

EXPOSE 5000