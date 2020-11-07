import threading
import pika
import yaml
import time

__config_file__ = './factory/config.yaml'


class Rabbit_cli:
    """ callback(worker_name, message) """

    def __init__(self, computer_name, callback_external=None):
        assert computer_name is not None
        self.computer = computer_name
        self.callback_external = callback_external
        with open(__config_file__, 'r') as f:
            content = yaml.load(f)
            self.usr_pub = content['pub']['usr']
            self.pwd_pub = content['pub']['pwd']
            self.host_pub = content['pub']['host']
            self.host_port = content['pub']['port']
            self.heartbeat = content['pub']['heartbeat']
        self.credentials = pika.PlainCredentials(self.usr_pub, self.pwd_pub)
        self.conn_param = pika.ConnectionParameters(
            host=self.host_pub, port=self.host_port, credentials=self.credentials, heartbeat=300)
        self.conn = None
        self.channel = None
        self.is_start = False

    def create_exchange(self, channel):
        channel.exchange_declare(exchange=self.computer, durable=False, exchange_type='fanout')


    def callback(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(method.delivery_tag, body.decode())
        if self.callback_external is not None:
            self.callback_external(self.computer, body.decode())

    def connect_init(self):
        self.conn = pika.BlockingConnection(self.conn_param)
        self.channel = self.conn.channel()
        self.create_exchange(self.channel)
        result_ = self.channel.queue_declare('', exclusive=True, auto_delete=True,
                                             arguments={'x-max-length': 10, 'x-overflow': 'drop-head'})
        self.channel.queue_bind(exchange=self.computer, queue=result_.method.queue)
        self.channel.basic_consume(result_.method.queue, self.callback)


    def _consuming(self):
        retry_counter = 0
        while self.is_start:
            try:
                self.connect_init()
                self.channel.start_consuming()
            except pika.exceptions.StreamLostError:
                print("rabbit error:StreamLostError")
                time.sleep(120)

                retry_counter += 1
                print("rabbit retry:", retry_counter)
            except pika.exceptions.ChannelWrongStateError:
                print("rabbit error:ChannelWrongStateError")
                time.sleep(120)
                retry_counter += 1
                print("rabbit retry:", retry_counter)
            except Exception as e:
                print("rabbit error:", retry_counter)
                time.sleep(120)
                retry_counter += 1
                print("rabbit retry:", retry_counter)

    def start(self):
        self.is_start = True
        threading.Thread(target=self._consuming).start()

    def stop(self):
        self.is_start = False
        self.channel.stop_consuming()

    def close(self):
        self.is_start =False
        self.channel.close()
        self.conn.close()

    # 先用celery获取在线列表，然后前端访问某monitor，
    # socket连接时，同时检查是否存在同computer monitor的数据获取，如果有则不做操作，如果没有则启动一个新的rabbit_cli。
    # rabbit_cli 获取到数据时，在sockets中匹配computer，进行boardnote thcast

# import wmi
# w = wmi.WMI()
# user = w.Win32_ComputerSystem()[0].UserName
#
# def cb(message):
#     print("m:",message)
#
# r = Rabbit_cli('worker1',cb)
# r.connect_init()
# r.start()
# r.stop()
# r.close()
