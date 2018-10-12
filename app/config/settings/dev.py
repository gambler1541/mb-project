from .base import *

secrets = json.load(open(os.path.join(SECRET_DIR, 'dev.json')))
DEBUG = True


# wsgi
WSGI_APPLICATION = 'config.wsgi.dev.application'
ALLOWED_HOSTS=[
]

# Database
DATABASES = secrets['DATABASES']



