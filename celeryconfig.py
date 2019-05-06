# Adding rabbitMQ info for broker settings.
# amqp://<username>:<password>@localhost:5672/<virtual_host>
#BROKER_URL = 'amqp://celeryuser:celery@localhost:5672/celeryvhost'
from datetime import timedelta
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
from celery.schedules import crontab
# Using the database to store task state and results
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_TIMEZONE = 'UTC'
# List of modules to import when celery starts.
CELERY_IMPORTS = ('tasks', )

CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

CELERYBEAT_SCHEDULE = {
    'add-every-1-hour': {
        'task': 'reportdaily',
        'schedule': timedelta(hours=1),
    },

    'midnight-task': {
        'task': 'midnightcleansing',
        'schedule': crontab(minute=0, hour=0)	,
    },

    # 'add-every-10-seconds': {
         # 'task': 'reportlive',
         # 'schedule': timedelta(seconds=20),
    # },


}


#command on windows
#celery -A tasks worker -l info -P eventlet
#celery -A tasks -l info beat



# app.conf.timezone = 'UTC'
# @app.on_after_configure.connect
# def setup_periodic_tasks(**kwargs):
#     # Calls test('hello') every 10 seconds.
#     app.add_periodic_task(10.0, beacon_activity.s('hello'))


# apt-get install rabbitmq-server
# http://erdemozkol.com/python-celery.html
# https://stackoverflow.com/questions/23050120/rabbitmq-command-doesnt-exist
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
# step 1: rabbitmq is up
# rabbitmq 1186 1 0 Nov12 ? 00:00:00 /bin/sh /usr/sbin/rabbitmq-server
# step2: execute tasks.py
# python tasks.py
# step3: start beat worker
# celery -A tasks -l info beat
# celery -A tasks -l info beat -s celerybeat-schedule
# or celery worker --loglevel=INFO -E
# celery -A tasks flower --port=5555
# http://docs.celeryproject.org/en/latest/userguide/monitoring.html#flower-real-time-celery-web-monitor
# celery inspect ping
# redis-server /usr/local/etc/redis.conf

# # Celery worker
# celery -A tasks worker -l info --concurrency=1
#
# # Celery beat (runs tasks by schedule)
# celery -A tasks beat --loglevel info
# celery -A tasks worker --loglevel=info --beat