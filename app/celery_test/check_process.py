from celery import Celery
from celery.schedules import crontab
import os

app = Celery('CelerySchedule',
             broker='redis://localhost',
             backend='redis://localhost')

app.conf.beat_schedule = {
    'add-every-morning': {
        'task': 'task.add',
        'schedule': crontab(hour=9, minute=55),
        'args': {16, 16}
    }
}

@app.task
def test(arg):
    print('run task: ', arg)