from .base import *

secrets = json.load(open(os.path.join(SECRET_DIR, 'production.json')))
DEBUG = False
ALLOWED_HOSTS=[
    'localhost',
]

# wsgi
WSGI_APPLICATION = 'config.wsgi.production.application'

# Database
DATABASES = secrets['DATABASES']





