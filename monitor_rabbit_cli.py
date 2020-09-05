import pika
import json
import threading

# producer
credentials = pika.PlainCredentials('root', 'root')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='106.14.20.200', port=5672, credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange=r'DESKTOP-QQDIIUS\\faker', durable=False, exchange_type='fanout')

for i in range(10):
    message = json.dumps({'OrderId': "x1000%s" % i})
# 向队列插入数值 routing_key是队列名
# delivery_mode = 2 声明消息在队列中持久化，delivery_mod = 1 消息非持久化。
    channel.basic_publish(exchange=r'DESKTOP-QQDIIUS\\faker', routing_key='', body=message,)
                          # properties=pika.BasicProperties(delivery_mode=1))
    print("send:",message)
connection.close()


# consumer
# 定义一个回调函数来处理消息队列中的消息，这里是打印出来
def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(body.decode(), method.delivery_tag)

credentials_cli = pika.PlainCredentials('root', 'root')
connection_cli = pika.BlockingConnection(pika.ConnectionParameters(host='106.14.20.200', port=5672, credentials=credentials_cli))
channel_cli = connection_cli.channel()
result_cli = channel_cli.queue_declare('', exclusive=True)
channel_cli.exchange_declare(exchange=r'DESKTOP-QQDIIUS\\faker', durable=False, exchange_type='fanout')
channel_cli.queue_bind(exchange=r'DESKTOP-QQDIIUS\\faker', queue=result_cli.method.queue)
channel_cli.basic_consume(result_cli.method.queue, callback)

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
def run():
    channel_cli.start_consuming()

threading.Thread(target=run).start()


channel_cli.stop_consuming()
connection_cli.close()