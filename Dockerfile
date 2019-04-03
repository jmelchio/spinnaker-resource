FROM python:3.7-alpine AS resource

COPY ./assets/check.py /opt/resource/check
COPY ./assets/in.py /opt/resource/in
COPY ./assets/out.py /opt/resource/out
RUN chmod 755 /opt/resource/*

FROM resource AS test
COPY ./test /test
RUN cd /test; set -e; for testfile in $(ls *.py); do \
        python -m unittest $testfile; \
    done


FROM resource
