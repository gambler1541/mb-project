from .base import *

DEBUG = False
ALLOWED_HOSTS=[
    'localhost',
]

# wsgi
WSGI_APPLICATION = 'config.wsgi.production.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}





