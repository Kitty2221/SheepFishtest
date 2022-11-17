FROM python:3.8-slim

RUN apt-get update && apt-get install -y gettext

ADD . /SheepFishtest

ENV PYTHONPATH ''${PYTHONPATH}/SheepFishtest''
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN chmod +x /SheepFishtest/docker/scripts/api.entrypoint.dev.sh && \
    chmod +x /SheepFishtest/docker/scripts/wait-for-it.sh

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /SheepFishtest/requirements.txt
