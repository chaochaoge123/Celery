
import pika
import uuid

class CMDRpcClient(object):
    def __init__(self):
        credentials = pika.PlainCredentials ('qqc','123')
        parameters = pika.ConnectionParameters (host ='127.0.0.1',credentials=credentials)
        self.connection= pika.BlockingConnection (parameters )
        self.channel = self.connection .channel()

        result = self.channel.queue_declare(exclusive= True )
        self.callback_queue=result .method.queue

        #声明要监听的callback_queue
        self.channel.basic_consume(self.on_response,no_ack=True,
                                   queue=self.callback_queue )

    def on_response(self,ch,method,props,body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode("gbk")

    def cal(self,n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange= '',
                                   routing_key= 'rpc_queue2',
                                   properties=pika.BasicProperties (
                                       reply_to=self.callback_queue ,
                                       correlation_id= self.corr_id,
                                   ),
                                   body=str(n))

        while self.response is None:
            self.connection .process_data_events()
            return self.response

cmd_rpc = CMDRpcClient ()
print("[x] Requesting fib(30)")
response = cmd_rpc.call('ipconfig')

print(response )















































































