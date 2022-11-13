from .settings import *  # noqa: F403, F401

DEBUG = False
CELERY_TASK_ALWAYS_EAGER = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
