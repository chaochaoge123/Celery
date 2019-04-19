
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




























