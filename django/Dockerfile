FROM python:2.7
ENV DJANGO_DEBUG=1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
RUN apt-get update && apt-get -y install nodejs npm
RUN npm install -g less
RUN ln -s /usr/bin/nodejs /usr/bin/node
