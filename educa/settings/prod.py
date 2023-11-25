import os
from .base import *


DEBUG = False

ADMINS = ('humoyun209', 'h.ahmedov209@gmail.com')

ALLOWED_HOSTS = ['*']


DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASS'),
        'HOST': 'db',
        'PORT': 5432
    }
}

