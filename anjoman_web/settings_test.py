from .settings import *
import tempfile

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': tempfile.NamedTemporaryFile(suffix='.sqlite3').name,
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


