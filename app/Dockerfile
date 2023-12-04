FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings_production

RUN mkdir /app
WORKDIR /app

RUN apk update && apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

COPY ./volumes/app/requirements/*.txt /app

RUN pip install --upgrade pip
RUN pip install -r prod.txt

CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 1; done && \
    python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py loaddata fixtures/sampledata.json && \
    gunicorn -b 0.0.0.0:8000 config.wsgi
