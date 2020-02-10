# use python 3 with Linux Alpine as environment.
# Python 3 is necessary because the script is written in python.
#FROM python:3-alpine
FROM python:3

WORKDIR /

#RUN apt-get install python3.7 python-pip

#RUN apk add make gcc musl-dev g++

# we need to install further python packages which are listed in requirements.txt
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install cython
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# install the german spacy model
RUN python -m spacy download de

# run the web server with python
WORKDIR /src
CMD [ "python", "-u", "./main.py" ]