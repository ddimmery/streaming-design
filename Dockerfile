# FROM python:3.7-alpine
FROM python:3.9-slim-buster
WORKDIR /code
# RUN apk add --no-cache gcc musl-dev linux-headers
# RUN apk add postgresql-dev python3-dev
# RUN apk add alpine-sdk
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
