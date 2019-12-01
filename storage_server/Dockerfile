FROM python:3.7

WORKDIR /application

## Install application requirements ##

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

## Run the application ##

COPY . .

ENV UWSGI_PROCESSES=1 \
    UWSGI_THREADS=2

VOLUME ["/spools"]

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["uwsgi"]
