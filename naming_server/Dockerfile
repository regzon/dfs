FROM python:3.7

WORKDIR /application

## Install application requirements ##

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

## Run the application ##

COPY . .

ENV DJANGO_SECRET_KEY= \
    DJANGO_ALLOWED_HOSTS= \
    DJANGO_DEBUG=False

VOLUME ["/spools"]

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["uwsgi"]
