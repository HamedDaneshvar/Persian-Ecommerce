FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings_local

RUN mkdir /app
WORKDIR /app

COPY ./volumes/app/requirements/*.txt /app

RUN pip install --upgrade pip
RUN pip install -r local.txt
RUN pip install gunicorn~=21.2.0

CMD python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py loaddata fixtures/sampledata.json; \
    gunicorn -b 0.0.0.0:8000 config.wsgi
