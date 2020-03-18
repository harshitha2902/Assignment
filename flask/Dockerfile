FROM ubuntu:16.04

MAINTAINER harshitha "hr569561@dal.ca"

RUN apt-get update && \
    apt-get install -y python3-pip -y
RUN apt-get install qunicorn3 -y

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app

Expose 5000

CMD ["gunicorn3","-b","0.0.0.0:5000","app:app","--workers=5"]