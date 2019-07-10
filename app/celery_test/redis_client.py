from __future__  import absolute_import, unicode_literals
import redis
from celery import  Celery


app = Celery('add',
             broker = 'redis://:800915@47.93.113.85:6379/0',
             backend = 'redis://:800915@47.93.113.85:6379/0')

@app.task
def add(x, y):
    print('running ....', x, y)
    return x + y





exit()
client = redis.StrictRedis(host = '47.93.113.85', password = 800915, port = 6379)
keys = client.keys()[0]
result = client.get(str(keys))

print(result)

# result = str(string, encoding='utf-8')