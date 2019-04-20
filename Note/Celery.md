## 1. 发布简单的任务流程(celery+redis)
```
(1)pip3 install celery

(2)任务文件tasks.py
import subprocess
from time import sleep
from celery import Celery

app = Celery('tasks',
             broker='redis://localhost',
             backend='redis://localhost',
            )

@app.task
def add(x, y):
    print("running...", x, y)
    return x + y

@app.task
def run_cmd(cmd):
    print("run ...%s" %cmd)
    sleep(5)
    cmd_obj =subprocess .Popen (cmd,shell=True,
                                stdout= subprocess .PIPE ,
                                stderr= subprocess .PIPE )
    return cmd_obj.stdout .read().decode('utf-8')  # 保证结果可进行序列化

'''
在当前目录开启celery服务
celery -A tasks worker --loglevel=info

注：win10上运行celery4.x会出现问题 要安装eventlet
celery -A tasks worker --loglevel=info -P eventlet

celery -A tasks worker --loglevel=debug  错误信息
'''

(3)启动celery 服务(在当前任务文件内执行)
celery -A tasks worker --loglevel=info

(4) 执行任务
t1.py
from tasks import add
# delay 将任务发到worker执行
res=add.delay(4,4)
print(res.get())  # 取值
print(res)

t2.py
from tasks import run_cmd
r=run_cmd.delay('dir')
print(r.get())

学习地址：
https://www.cnblogs.com/alex3714/p/6351797.html
```
## 2. 定时任务
```
periodic_task.py

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

# https://blog.csdn.net/Shyllin/article/details/80940643
```












































































