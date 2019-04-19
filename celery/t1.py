from celery.tasks import  add ,hostname
r=add.delay(4,4)
r.ready()

b= hostname .delay()
c =b.result
print(c)









