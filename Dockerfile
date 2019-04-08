FROM python:3.7-alpine AS resource

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
COPY ./assets/check.py /opt/resource/check
COPY ./assets/inscript.py /opt/resource/in
COPY ./assets/out.py /opt/resource/out
RUN chmod 755 /opt/resource/*

FROM resource AS test
COPY ./test /test
COPY ./assets /assets
RUN cd /; set -e; \
          python -m unittest test.testin.TestTimeOut; \
          python -m unittest test.testin.TestIn; \
          python -m unittest test.testcheck.TestTimeOut; \
          python -m unittest test.testcheck.TestCheck

FROM resource
