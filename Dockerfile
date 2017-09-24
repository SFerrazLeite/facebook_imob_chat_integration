FROM python:3.6.1-alpine
MAINTAINER iMobility GmbH <backend@i-mobility.at>

# core dependencies
RUN apk add --update --no-cache ca-certificates

# build dependencies
RUN apk add --update --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    make

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install requirements
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir -r requirements-prod.txt

# clean up
RUN apk del .build-deps

# declare public port
EXPOSE 80

# default entry point
CMD gunicorn facebook_imob_chat_integration.app:app --bind 0.0.0.0:80 --worker-class aiohttp.GunicornUVLoopWebWorker

# copy application source
COPY ./ ./

# install application
RUN pip install --no-cache-dir -e .
