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