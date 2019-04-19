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


