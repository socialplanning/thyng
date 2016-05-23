FROM python:2.7
RUN mkdir /code
WORKDIR /code
ADD ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
RUN apt-get update && apt-get install -y postgresql-client
ADD . /code/
RUN mkdir -p /srv/my-sites

