# pull official base image
FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update
RUN apt-get install -y gcc libpq-dev 

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt
RUN apt-get autoremove -y gcc

# copy project
COPY . /usr/src/app/

ENTRYPOINT ["python3", "run.py", "dev"]
