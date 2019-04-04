FROM python:3.7-alpine AS resource

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
COPY assets /opt/resource/check
COPY assets /opt/resource/in
COPY assets /opt/resource/out
RUN chmod 755 /opt/resource/*

FROM resource AS test
COPY test /test
COPY assets /assets
RUN cd /; python -m unittest discover


FROM resource
