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

# 取信息
channel.basic_consume('hello_one',
                      callback,    # 取到消息后调用callback
                      #no_ack=True   # 消息处理后，不向rabbit-server确认消息已消费完毕
                    )
print('[*] waiting for messages. To exit press CTRL+C')

# 阻塞模式
channel .start_consuming()
