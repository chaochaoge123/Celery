
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



















