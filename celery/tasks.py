import subprocess
from time import sleep
import sqlalchemy as sa

from celery import Celery

backend = 'db+mysql://root:@127.0.0.1/celery'
broker = 'amqp://guest@127.0.0.1:5672'
app = Celery('tasks',backend = backend ,broker= broker )

@app.task
def add(x,y):
    sleep(10)
    return x + y


@app.task
def hostname():
    return subprocess .check_output(['hostname'])



