FROM python:3.9.19-alpine

LABEL maintainer Matthew Zhao
COPY app .
RUN pip3 install -r requirements.txt &&\
    mkdir -p /etc/varta/

CMD python3 main.py