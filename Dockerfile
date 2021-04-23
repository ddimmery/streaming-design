FROM python:3-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps build-base gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
ENV DESIGN_NAME=bwd
ENV PROCESSOR_NAME=yaml
ENV PYTHONUNBUFFERED=1
COPY . .
