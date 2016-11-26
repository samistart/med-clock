FROM ubuntu:14.04
MAINTAINER 5bitz <samistart@hotmail.com>

# no tty
ENV DEBIAN_FRONTEND noninteractive

# get up to date
RUN apt-get -qq update --fix-missing

# Bootstrap the image so that it includes all of our dependencies
RUN apt-get -qq install python-dev python-virtualenv --assume-yes

# copy the contents of the `app/` folder into the container at build time
ADD . /app/

# create a virtualenv we can later use
RUN mkdir -p /venv/
RUN virtualenv /venv/

RUN apt-get install python-dev
RUN apt install -y libpq-dev python3-dev

RUN /bin/bash --rcfile venv/bin/activate

# install python dependencies from pypi into venv
RUN /venv/bin/pip install -r /app/requirements.txt

# expose a port for the flask development server
EXPOSE 5000

# run our flask app inside the container
CMD cd /app/ && /venv/bin/python app.py
