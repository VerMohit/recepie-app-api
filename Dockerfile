# python = name of docker image
# 3.9-alpine3.13 = the name of tag we're using
# alpine = lightweight version of linux and ideal for running docker containers (has bare min. requireements for image)
FROM python:3.9-alpine3.13
#LABEL authors="mohit"
LABEL maintainer="mohit"

# Recommended when running python in docker container
# output of python directly printed to stdout, prventing message delay to screen (logs are immediately seen)
ENV PYTHONUNBUFFERED 1

# copy requirements.txt into /tmp/requirements.txt (docker image)
COPY ./requirements.txt /tmp/requirements.txt

# copy requirements.dev.txt into /tmp/requirements.dev.txt (docker image) to have avilable during build phase
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# copy app dir, containing django app into docker container /app
COPY ./app /app
# default dir where commands will be run from in the docker image. Same lcoation as where django project is linked to
WORKDIR /app
# access port 8000 using image
EXPOSE 8000

# setting build arg to false. When used in out docker-compose config, it will be true. In other docker-compose config, it will be false
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
      then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
      --disabled-password \
        --no-create-home \
        django-user

# updates ENV variable inside image
ENV PATH="/py/bin:$PATH"

# Specifies user we are switching to. Everything prior to this line, is using the root user
# When we reach this line, anything run from the docker image will be run as django-user
USER django-user