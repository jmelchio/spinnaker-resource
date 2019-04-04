FROM python:3.7-alpine AS resource

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
COPY assets /opt/resource/check
COPY assets /opt/resource/in
COPY assets /opt/resource/out
RUN chmod 755 /opt/resource/*

FROM resource AS test
COPY test /test
RUN cd /test; set -e; for testfile in $(ls *.py); do \
        python -m unittest $testfile; \
    done


FROM resource
