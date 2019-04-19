## 1.消息确认消费
```
1. 生产者端发消息时，加参数 
		  properties=pika.BasicProperties(
		  delivery_mode=2,  # make message persistent
	  ),
	  
2. 消费者端，消息处理完毕时，发送确认包
		ch.basic_ack(delivery_tag=method.delivery_tag)

		
生产者端：
import pika

credentials = pika.PlainCredentials('qqc', '123')

parameters = pika.ConnectionParameters(host='127.0.0.1',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

#声明queue
channel.queue_declare(queue='hello_one',durable=True )  # durable==True 队列持久化

channel.basic_publish(exchange='',
                      routing_key='hello_one', #路由
                      properties = pika.BasicProperties (
                          delivery_mode= 2 ,  # 将消息持久化
                      ),
                      body='Hello World')

print(" [x] Sent 'Hello World!'")

connection.close()


消费者端：
import pika
import time

credentials = pika.PlainCredentials ('qqc','123')

parameters = pika.ConnectionParameters (host='localhost',credentials =credentials )
connection = pika.BlockingConnection (parameters )

 # 队列连接通道
channel = connection .channel()

def callback(ch,method,properties,body):
    '''
    :param ch: 通道
    :param method: 请求方法
    :param properties: 消息参数
    :param body:  消息内容
    :return:
    '''
    print("[x] received %r" % body,method )
    time.sleep(10)
    print('msg handle done...',body)

    # 消费者处理完毕向服务端返回确认包，清除队列消息
    ch.basic_ack(delivery_tag= method .delivery_tag)

# 取信息
channel.basic_consume('hello_one',
                      callback,    # 取到消息后调用callback
                      #no_ack=True   # 消息处理后，不向rabbit-server确认消息已消费完毕
                    )
print('[*] waiting for messages. To exit press CTRL+C')

# 阻塞模式
channel .start_consuming()
```
## 2. 公平分发
```
消费者端
	channel.basic_qos(prefetch_count=1)
	
代码：
import pika
import time

credentials = pika.PlainCredentials ('qqc','123')

parameters = pika.ConnectionParameters (host='localhost',credentials =credentials )
connection = pika.BlockingConnection (parameters )

 # 队列连接通道
channel = connection .channel()

def callback(ch,method,properties,body):
    '''
    :param ch: 通道
    :param method: 请求方法
    :param properties: 消息参数
    :param body:  消息内容
    :return:
    '''
    print("[x] received %r" % body,method )
    # time.sleep(10)
    print('msg handle done...',body)

    # 消费者处理完毕向服务端返回确认包，清除队列消息
    ch.basic_ack(delivery_tag= method .delivery_tag)

# 公平分发
channel.basic_qos(prefetch_count=1)

# 取信息
channel.basic_consume('hello_one',
                      callback,    # 取到消息后调用callback
                      #no_ack=True   # 消息处理后，不向rabbit-server确认消息已消费完毕
                    )
print('[*] waiting for messages. To exit press CTRL+C')

# 阻塞模式
channel .start_consuming()
```
## 3. exchange 
```
exchange type 
	fanout = 广播
	direct = 组播
	topic  = 规则播 
	header = 
	
```
### 3.1 fanout
```
生产者：
import pika
import sys
credentials = pika.PlainCredentials('qqc', '123')

parameters = pika.ConnectionParameters(host='127.0.0.1',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

channel .exchange_declare(exchange= 'logs',exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello world" # 打印跟的参数

# 绑定exchange的所有队列都收到消息
channel .basic_publish(exchange= 'logs',
                       routing_key= '',
                       body =message )
print(" [x] Sent %r" % message)

connection.close()

'''
微博应用
发一个动态，关注的好友被推送，没有登陆的好友不推送
'''


消费者：
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

```
### 3.2 direct
```
发布者：
import pika
import sys
credentials = pika.PlainCredentials('qqc', '123')

parameters = pika.ConnectionParameters(host='127.0.0.1',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

channel .exchange_declare(exchange= 'direct_logs',exchange_type='direct')

log_level =sys.argv[1] if len(sys.argv)> 1 else 'info'
message = ' '.join(sys.argv[1:]) or "info: Hello world" # 打印跟的参数

channel .basic_publish(exchange= 'logs',
                       routing_key= log_level ,
                       body =message )
print(" [x] Sent %r" % message)

connection.close()

# python3 P_direct.py info hello  在info上发消息


订阅者：
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

# python3 .\C_direct.py info  接收info上的消息
```
### 3.3 topic
```
发布者：
import pika
import sys

credentials = pika.PlainCredentials('qqc', '123')

parameters = pika.ConnectionParameters(host='127.0.0.1',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection .channel()

channel.exchange_declare(exchange= 'topic_log',exchange_type='topic')

log_level = sys.argv[1] if len(sys.argv) >1 else 'all.info'

message = ' '.join(sys.argv[1:]) or 'all.info:Hello World'

channel .basic_publish(exchange='topic_log',
                       routing_key= log_level ,
                       body = message)
print("[x] Sent %r" %message)
connection .close()



订阅着：
import pika,sys
credentials = pika.PlainCredentials('qqc', '123')

parameters = pika.ConnectionParameters(host='127.0.0.1',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道
queue_obj = channel .queue_declare(queue = '',exclusive= True )
queue_name = queue_obj.method.queue


log_levels = sys.argv[1:]

if not log_levels :
    sys.stderr .write("User: %s [info] [warning] [error]\n" % sys.argv[0])

for level in log_levels :
    channel .queue_bind(exchange= 'topic_log',
                        queue = queue_name ,
                        routing_key= level)
print('[*] Waiting for logs.To exit press CTRL+C')


def callback(ch,method,properties,body):
    print("[x] %r" %body)

channel .basic_consume(queue_name ,callback )
channel .start_consuming()



测试：
发布者：
python3 P_topic.py i.mysql.error tttttt

订阅者：
python3 C_topic.py *.mysql.error
```
## 4. RPC























































