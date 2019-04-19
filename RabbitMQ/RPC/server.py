
import subprocess
import pika
import time

credentials = pika.PlainCredentials ('qqc','123')

parameters = pika.ConnectionParameters(host='127.0.0.1',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

channel .queue_declare(queue='rpc_queue2')

def fib(n):
    if n == 0:
        return 0
    elif n ==1:
        return 1
    else:
        return fib(n-1)+fib(n-2)


def run_cmd(cmd):
    cmd_obj = subprocess .Popen (cmd,shell = True ,
                                 stdout= subprocess .PIPE ,
                                 stderr=subprocess .PIPE )
    result = cmd_obj.stdout .read() + cmd_obj.stderr .read()
    return result

def on_request(ch,method,props,body):
    cmd = body.decode('utf-8')

    print('[.]run(%s)'%cmd)
    response = run_cmd(cmd)

    ch.basic_publish(exchange= '',
                     routing_key= props.reply_to,
                     properties=pika.BasicProperties (correlation_id= props.correlation_id),
                     body=response )

    ch.basic_ack(delivery_tag= method .delivery_tag)

channel .basic_consume(on_request,queue='rpc_queue2')
print('[x] Awaiting RPC requests')
channel .start_consuming()



































