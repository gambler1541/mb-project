from .base import *

DEBUG = True


# wsgi
WSGI_APPLICATION = 'config.wsgi.dev.application'
ALLOWED_HOSTS=[
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



