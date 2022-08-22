FROM alpine:3.16

ENV PYTHONUNBUFFERED=1
ENV LANG=en

RUN apk add --no-cache python3 py3-openssl
RUN python3 -m ensurepip --upgrade
RUN pip3 install --disable-pip-version-check --no-cache-dir html5lib html2text requests

ADD gogrepoc.py /
ENTRYPOINT ["python3", "/gogrepoc.py"]

WORKDIR /srv
