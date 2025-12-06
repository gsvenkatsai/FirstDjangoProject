from .common import *
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@ivmd-$8*7#0fi1fl!-*n6)a(%!99v24l3f3xuv@o8e%13rm9^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'firstproject3',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'Venkat#O1',
        
    }
}