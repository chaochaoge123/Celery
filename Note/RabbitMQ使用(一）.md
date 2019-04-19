## 1. 安装与使用
```
1. 激活 RabbitMQ's Management Plugin (前面跟绝对路径)
"D:\娱乐\rabbitmq_server-3.6.5\sbin\rabbitmq-plugins.bat" enable rabbitmq_management

2 .用管理员权限启动服务(在\sbin\路径下下操作)
net stop RabbitMQ && net start RabbitMQ

3. 创建用，密码，角色
(1) 查看用户，角色
rabbitmqctl.bat list_users
(2) 新增用户
rabbitmqctl.bat add_user username password
(3)绑定用户角色
rabbitmqctl.bat set_user_tags 用户名 administrator
多个角色：
rabbitmqctl.bat  set_user_tags  username tag1 tag2 ...
(4)修改密码
rabbitmqctl change_password userName newPassword
(5)删除用户
rabbitmqctl.bat delete_user username
(6) 查看队列状态
rabbitmqctl list_queues

4. 后台管理
 http://localhost:15672 
```
## 2. 角色分类
```
(1) 超级管理员(administrator)

可登陆管理控制台(启用management plugin的情况下)，可查看所有的信息，并且可以对用户，策略(policy)进行操作。

(2) 监控者(monitoring)

可登陆管理控制台(启用management plugin的情况下)，同时可以查看rabbitmq节点的相关信息(进程数，内存使用情况，磁盘使用情况等) 

(3) 策略制定者(policymaker)

可登陆管理控制台(启用management plugin的情况下), 同时可以对policy进行管理。

(4) 普通管理者(management)

仅可登陆管理控制台(启用management plugin的情况下)，无法看到节点信息，也无法对策略进行管理。

(5) 其他的

无法登陆管理控制台，通常就是普通的生产者和消费者。

```
## 3. 用户权限设置
```
用户对exchange,queue的操作权限，包含配置权限，读写权限
配置权限会影响到exchange，queue的声明和删除。读写权限影响到从queue里取消息，向exchange发送消息以及queue和exchange的绑定(bind)操作

相关操作：
(1) 设置用户权限
rabbitmqctl  set_permissions  -p  VHostPath  User  ConfP  WriteP  ReadP

rabbitmqctl set_permissions -p / qqc ".*" ".*" ".*"

(2) 查看(指定hostpath)所有用户的权限信息
rabbitmqctl  list_permissions  [-p  VHostPath]

(3) 查看指定用户的权限信息
rabbitmqctl  list_user_permissions  User

(4)  清除用户的权限信息
rabbitmqctl  clear_permissions  [-p VHostPath]  User
```
## 4. pika 实现生产者消费者
```
生产者端：
import pika

credentials = pika.PlainCredentials('qqc', '123')

parameters = pika.ConnectionParameters(host='127.0.0.1',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

#声明queue
channel.queue_declare(queue='hello_one',durable=True) # durable==True 队列持久化

channel.basic_publish(exchange='',
                      routing_key='hello_one', #路由
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
    print("[x] received %r" % body,ch,method,properties)
    # time.sleep(10)
    # print('msg handle done...',body)
    # ch.basic_ack(delivery_tag= method .delivery_tag)

# 取信息
channel.basic_consume('hello_one',
                      callback,    # 取到消息后调用callback
                      no_ack=True  # 消息处理后，不向rabbit-server确认消息已消费完毕
                      )
print('[*] waiting for messages. To exit press CTRL+C')

# 阻塞模式
channel .start_consuming()


```





























