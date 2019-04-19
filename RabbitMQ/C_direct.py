import pika
import time
import sys
credentials = pika.PlainCredentials ('qqc','123')

parameters = pika.ConnectionParameters (host='localhost',credentials =credentials )
connection = pika.BlockingConnection (parameters )

 # 队列连接通道
channel = connection .channel()

channel .exchange_declare(exchange='logs',exchange_type='fanout')

#不指定queue名字，rabbit会随机分配一个名字
# exclusive=True会在使用此queue的消费者断开后,自动将queue删除
queue_obj = channel .queue_declare(queue='',exclusive= True)

queue_name = queue_obj .method.queue
print('queue name',queue_name,queue_obj )

log_levels = sys.argv[1:]

if not log_levels :
    sys.stderr .write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit()

for level in log_levels :
    channel.queue_bind(exchange='logs',
                       queue=queue_name,
                       routing_key= level) # 绑定队列到exchange

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch,method,properties,body):
    print(body)

channel .basic_consume(queue_name, callback)

# 阻塞模式
channel .start_consuming()

'''
发布订阅模式
绑定且在线才能收到
'''