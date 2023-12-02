from kombu import Exchange, Queue

BROKER_URL = 'pyamqp://guest:guest@localhost//'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'  # Use Redis as the result backend

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

CELERY_DISABLE_RATE_LIMITS = True
CELERY_IGNORE_RESULT = True
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERYD_PREFETCH_MULTIPLIER = 1
