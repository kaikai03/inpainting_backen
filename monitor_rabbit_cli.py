
import threading
import pika
import yaml

__config_file__ = 'config.yaml'


class Rabbit_cli:
    """ callback(message) """
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
        self.exchange_created = False
        self.conn = None
        self.channel = None

    def create_exchange(self, channel):
        if not self.exchange_created:
            channel.exchange_declare(exchange=self.computer,
                                     durable=False, exchange_type='fanout')
            self.exchange_created = True

    def connect_init(self):
        def callback(ch, method, properties, body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(method.delivery_tag, body.decode())
            if self.callback_external is not None:
                self.callback_external(body.decode())

        self.conn = pika.BlockingConnection(self.conn_param)
        self.channel = self.conn.channel()
        self.create_exchange(self.channel)
        result_ = self.channel.queue_declare('', exclusive=True, auto_delete=True,
                                             arguments={'x-max-length': 10, 'x-overflow': 'drop-head'})
        self.channel.queue_bind(exchange=self.computer, queue=result_.method.queue)
        self.channel.basic_consume(result_.method.queue, callback)

    def start(self):
        assert self.channel is not None
        assert self.channel.is_open
        threading.Thread(target=lambda: self.channel.start_consuming()).start()

    def stop(self):
        self.channel.stop_consuming()

    def close(self):

        self.channel.close()
        self.conn.close()



# import wmi
# w = wmi.WMI()
# user = w.Win32_ComputerSystem()[0].UserName
#
# def cb(message):
#     print("m:",message)
#
# r = Rabbit_cli(user,cb)
# r.start()
# r.connect_init()
# r.start()
# r.stop()
# r.close()