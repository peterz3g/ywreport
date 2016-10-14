FROM daocloud.io/python:2.7
MAINTAINER peterz3g <peterz3g@163.com>


RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/requirements.txt
RUN pip install Django==1.9.8
RUN pip install -r /code/requirements.txt
COPY . /code
COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

CMD /code/docker-entrypoint.sh
