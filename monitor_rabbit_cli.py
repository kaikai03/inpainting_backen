from monitor_tmp import Monitor
import threading

import pika
import json

# producer
credentials = pika.PlainCredentials('root', 'root')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='106.14.20.200', port=5672, credentials=credentials, heartbeat=300))
channel = connection.channel()
channel.exchange_declare(exchange=r'DESKTOP-QQDIIUS\\faker', durable=False, exchange_type='fanout')

for i in range(10):
    message = json.dumps({'OrderId': "x1000%s" % i})
# 向队列插入数值 routing_key是队列名
# delivery_mode = 2 声明消息在队列中持久化，delivery_mod = 1 消息非持久化。
    channel.basic_publish(exchange=r'DESKTOP-QQDIIUS\\faker', routing_key='', body=message,
                          properties=pika.BasicProperties(delivery_mode=1))
    print("send:",message)

connection.close()

connection.is_closed
channel.is_closed


# consumer
# 定义一个回调函数来处理消息队列中的消息，这里是打印出来
def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(method.delivery_tag, body.decode())

credentials_cli = pika.PlainCredentials('root', 'root')
connection_cli = pika.BlockingConnection(pika.ConnectionParameters(
    host='106.14.20.200', port=5672, credentials=credentials_cli, heartbeat=10))
channel_cli = connection_cli.channel()
result_cli = channel_cli.queue_declare('', exclusive=True, auto_delete=True,
                                       arguments={'x-max-length': 10, 'x-overflow': 'drop-head'})
channel_cli.exchange_declare(exchange=r'DESKTOP-QQDIIUS\\faker', durable=False, exchange_type='fanout')
channel_cli.queue_bind(exchange=r'DESKTOP-QQDIIUS\\faker', queue=result_cli.method.queue)
channel_cli.basic_consume(result_cli.method.queue, callback)

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
def run():
    channel_cli.start_consuming()

threading.Thread(target=run).start()


channel_cli.stop_consuming()
connection_cli.close()

connection_cli.is_closed
channel_cli.is_closed

import time
monitor = Monitor()
timer = None
def reporter_start():
    # channel.basic_publish(exchange=r'DESKTOP-QQDIIUS\\faker', routing_key='', body=json.dumps(monitor.get_report()),
    #                       properties=pika.BasicProperties(delivery_mode=1))
    channel.basic_publish(exchange=r'DESKTOP-QQDIIUS\\faker', routing_key='', body=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                          properties=pika.BasicProperties(delivery_mode=1))

    global timer
    timer = threading.Timer(60, reporter_start)
    timer.start()
reporter_start()


while(timer.is_alive()):
    timer.cancel()
    timer.cancel()
