import sys

from .base import *

secrets = json.load(open(os.path.join(SECRET_DIR, 'production.json')))



DEBUG = False
ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']


RUNSERVER = 'runserver' in sys.argv
ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']

if RUNSERVER:
    DEBUG = True
    ALLOWED_HOSTS =[
        'localhost',
        '127.0.0.1',
    ]


# django-storages
INSTALLED_APPS += [
    'storages',
]

DATABASES = secrets['DATABASES']

DEFAULT_FILE_STORAGE = 'config.storages.S3DefaultStorage'
STATICFILES_STORAGE = 'config.storages.S3StaticStorage'

AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']
AWS_DEFAULT_ACL = secrets['AWS_DEFAULT_ACL']
AWS_S3_REGION_NAME = secrets['AWS_S3_REGION_NAME']
AWS_S3_SIGNATURE_VERSION = secrets['AWS_S3_SIGNATURE_VERSION']

# wsgi
WSGI_APPLICATION = 'config.wsgi.production.application'

# Database
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')

# log
LOG_DIR = '/var/log/django'
# if not os.path.exists(LOG_DIR):
#     LOG_DIR = os.path.join(ROOT_DIR, '.log')
#     if not os.path.exists(LOG_DIR):
#         os.mkdir(LOG_DIR)

if not os.path.exists(LOG_DIR):
    LOG_DIR = os.path.join(ROOT_DIR,'.log')
    os.makedirs(LOG_DIR, exist_ok=True)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            'format': '[%(asctime)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'django.server',
            'backupCount': 10,
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': 10485760,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_error'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}




