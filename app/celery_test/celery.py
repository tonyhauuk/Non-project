from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('project', broker='redis://800915@47.93.113.85:6379/0', backend='redis://800915@47.93.113.85:6379/0', include=['project.tasks'])

app.conf.update(result_expires = 3600)

if __name__ == '__main__':
    app.start()