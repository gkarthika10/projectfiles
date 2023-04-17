from email.policy import default
from .base import *

DEBUG = config('DEBUG', cast=bool, default=True)
ALLOWED_HOSTS = ['54.236.69.41','127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'salesforce': {
        'ENGINE': 'salesforce.backend',
        'CONSUMER_KEY': config('CONSUMER_KEY'),               
        'CONSUMER_SECRET': config('CONSUMER_SECRET'),            
        'USER': config('SFUSER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': 'https://test.salesforce.com/',
    }
}

DATABASE_ROUTERS = [
    "salesforce.router.ModelRouter"
]

