from .settings import *
import tempfile

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': tempfile.NamedTemporaryFile(suffix='.sqlite3').name,
    }
}

# Use a simple password hasher for testing purposes
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]


# Use the console email backend to avoid sending real emails during tests
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# python manage.py test --settings=anjoman_web.settings_test
