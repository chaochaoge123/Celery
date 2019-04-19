
import pika

credentials = pika.PlainCredentials('qqc', '123')

parameters = pika.ConnectionParameters(host='127.0.0.1',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

#声明queue
channel.queue_declare(queue='hello_one',durable=True )  # durable==True 队列持久化

channel.basic_publish(exchange='',
                      routing_key='hello_one', #路由
                      body='Hello World')

print(" [x] Sent 'Hello World!'")

connection.close()
