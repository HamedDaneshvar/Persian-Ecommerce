from .settings import *


DEBUG = False

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':  config("POSTGRES_DB", default="db_name"),
        'USER': config("POSTGRES_USER", default="postgres"),
        'PASSWORD': config("POSTGRES_PASSWORD", default="db_password"),
        'HOST': config("POSTGRES_HOST", default="127.0.0.1"),
        'PORT': config("POSTGRES_PORT", default="5432"),
    }
}
