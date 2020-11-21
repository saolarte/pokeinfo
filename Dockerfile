FROM python:3.6

COPY ./requirements.txt /requirements.txt
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
WORKDIR /app
RUN apt-get update \
    # && apt-get install -y python-pip \
    && apt-get install -y libpq-dev

RUN pip install -r /requirements.txt

RUN chmod -x /docker-entrypoint.sh
CMD ["sh", "/docker-entrypoint.sh"]
