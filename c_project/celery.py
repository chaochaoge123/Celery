from __future__ import absolute_import ,unicode_literals
from celery import Celery

app = Celery('c_project',
             broker='redis://localhost',
             backend='redis://localhost',
             include= ['c_project.tasks'])

app.conf.update(
    result_expires = 3600,
)

if __name__ == '__main__':
    app.start()











































