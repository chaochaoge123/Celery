import pika
import time

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

# 绑定队列都exchange
channel .queue_bind(exchange= 'logs',queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch,method,properties,body):
    print(body)

# 阻塞模式
channel .start_consuming()
