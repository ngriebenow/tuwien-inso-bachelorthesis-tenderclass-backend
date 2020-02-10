# use python 3 with Linux Alpine as environment.
# Python 3 is necessary because the script is written in python.
# Alpine is a lightweight version of Linux which is sufficient for this audio converting service
FROM python:3-alpine

WORKDIR /

# we need to install further python packages which are listed in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# install the german spacy model
RUN python -m spacy download de

# run the web server with python
RUN cd src
CMD [ "python", "-u", "./main.py" ]