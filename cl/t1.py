from tasks import add
# delay 将任务发到worker执行
res=add.delay(4,4)
print(res.get())  # 取值
print(res)










