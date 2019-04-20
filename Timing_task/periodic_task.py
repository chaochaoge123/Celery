# coding:utf-8

# 拒绝隐式引入，因为celery.py的名字和celery的包名冲突，需要使用这条语句让程序正确地运行
from __future__ import absolute_import
from celery import Celery
from celery.schedules import  crontab

app = Celery ()
@app.on_after_configure .connect
def setup_periodic_tasks(sender,**kwargs ):
    # 每隔10秒打印hello
    sender .add_periodic_task(10.0,test.s('hello'),name='add every 10')

    # 隔30秒打印world
    sender.add_periodic_task (30.0,test.s('world'),expires=10)

    # 每周一早上7：30 执行
    sender.add_periodic_task (
        crontab(hour=7,minute= 30,day_of_week=1),
        test.s('Happy Mondays')

    # sender .add_periodic_task (10.0,add.s(3,4))
    )

@app.task
def test(arg):
    print(arg)

@app.task
def add(x, y):
    print(x+y)
    return x + y

app.conf.beat_schedule={
'add-every-30-seconds':{
    'task':'add',
    # 'schedule':20.0, # 每20秒调用tasks.add
    "schedule": crontab(minute="*/1"), # 每分钟执行
    'args':(16,16)
},
}
app.conf.timezone = 'UTC'

'''
发布任务：
celery -A periodic_task beat

执行任务：
celery -A periodic_task worker -P eventlet

合并：worker和beat一起启动
celery -B -A periodic_task worker --loglevel=info
'''
































