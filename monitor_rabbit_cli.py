import pika
import json
import threading

# producer
credentials = pika.PlainCredentials('root', 'root')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='106.14.20.200', port=5672, credentials=credentials))
channel = connection.channel()
# 声明消息队列，消息将在这个队列传递，如不存在，则创建
result = channel.queue_declare(queue=r'DESKTOP-QQDIIUS\\faker')

for i in range(10):
    message = json.dumps({'OrderId':"x1000%s"%i})
# 向队列插入数值 routing_key是队列名
    channel.basic_publish(exchange='', routing_key=r'DESKTOP-QQDIIUS\\faker', body=message)
    print("send:",message)
connection.close()


# consumer
# 定义一个回调函数来处理消息队列中的消息，这里是打印出来
def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(body.decode())

credentials_cli = pika.PlainCredentials('root', 'root')
connection_cli = pika.BlockingConnection(pika.ConnectionParameters(host='106.14.20.200', port=5672, credentials=credentials_cli))
channel_cli = connection_cli.channel()
channel_cli.queue_declare(queue=r'DESKTOP-QQDIIUS\\faker', durable=False)
channel_cli.basic_consume(r'DESKTOP-QQDIIUS\\faker', callback)

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
def run():
    channel_cli.start_consuming()

t1 = threading.Thread(target=run)
t1.start()

channel_cli.stop_consuming()
connection_cli.close()