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
