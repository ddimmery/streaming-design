FROM python:3.9-slim-buster
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV DESIGN_NAME=bwd
ENV PROCESSOR_NAME=yaml
ENV PYTHONUNBUFFERED=1
COPY . .
