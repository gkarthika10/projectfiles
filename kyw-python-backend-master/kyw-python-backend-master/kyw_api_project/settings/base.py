import os
from pathlib import Path
from decouple import config
from corsheaders.defaults import default_headers
import rootpath
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'salesforce',
    'django_salesforce_oauth',
    'rest_framework',
    'corsheaders',
    'usermanagement_api',
    'django_rest_passwordreset',
    'auction_api',
    'candidate_api',
    'resumeparser',
    'employer_api',
    'opscentre_usermanagement_api',
    "django_celery_beat",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters':{
        'main_formatter': {
            'format' : "{asctime} - {levelname} - {module} - {funcName} - {message}",
            "style" : "{",
        },
    },
    'handlers': {
        'console': {
            'class': "logging.StreamHandler",
            'formatter': 'main_formatter',
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'app_log.log',
            'when': 'D',
            'backupCount': 10, # keep at most 10 log files
            'formatter': 'main_formatter'
            }
        # 'file': {
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': 'debug.log',
        #     'backupCount': 10, # keep at most 10 log files
        #     'maxBytes': 1024, # 5*1024*1024 bytes (5MB)
        #     }
        # 'file': {
        #     'class': 'logging.FileHandler',
        #     'filename': 'kyw_logs_' + test['date'] + '.log',
        #     'formatter': 'main_formatter',
        # },
    },
    'loggers': {
        'main': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

ROOT_URLCONF = 'kyw_api_project.urls'
TEMP_PATH =rootpath.get_project_root()
TEMPLATE_DIR = os.path.join( TEMP_PATH, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

WSGI_APPLICATION = 'kyw_api_project.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'


EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = 'localhost:3000',
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000'
# ]

CORS_ORIGIN_WHITELIST = ['127.0.0.1:3000', '127.0.0.1:3001', '54.236.69.41:3001', '54.236.69.41:3001', '54.236.69.41:8000', '54.236.69.41:8001']
CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:3000', 'http://127.0.0.1:3001', 'http://54.236.69.41:3000', 'http://54.236.69.41:3001', 'http://54.236.69.41:8000', 'http://54.236.69.41:8001']

CORS_ALLOW_CREDENTIALS = True
#CORS_ALLOW_HEADERS = ["*"]

CORS_ALLOW_HEADERS = list(default_headers) + [
    "userType",
    "aucstage",
]
