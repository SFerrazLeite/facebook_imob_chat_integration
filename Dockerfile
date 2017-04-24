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
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy application source
COPY ./ ./

# install application
RUN pip install --no-cache-dir -e . && pip install --no-cache-dir .[production]

# clean up
RUN apk del .build-deps

EXPOSE 80
CMD gunicorn imob_async_service.app:app --bind 0.0.0.0:80 --worker-class aiohttp.GunicornUVLoopWebWorker
