# coding: utf-8

import pika
import yaml

__config_file__ = 'config.yaml'


class Publisher:
    def __init__(self, computer_name):
        assert computer_name is not None
        self.computer = computer_name
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

    def create_exchange(self, channel):
        if not self.exchange_created:
            channel.exchange_declare(exchange=self.computer,
                                     durable=False, exchange_type='fanout')
            self.exchange_created = True

    def connect(self):
        self.conn = pika.BlockingConnection(self.conn_param)
        self.channel = self.conn.channel()
        self.create_exchange(self.channel)

    def publish_long(self, message):
        try:
            if self.conn.is_closed or (not self.exchange_created):
                self.connect()
            self.channel.basic_publish(exchange=self.computer,
                                       routing_key='', body=message,
                                       properties=pika.BasicProperties(delivery_mode=1))
        except Exception as e:
            self.connect()
            self.channel.basic_publish(exchange=self.computer,
                                       routing_key='', body=message,
                                       properties=pika.BasicProperties(delivery_mode=1))

    def publish_temp(self, message):
        try:
            conn_ = pika.BlockingConnection(self.conn_param)
            channel_ = conn_.channel()
            self.create_exchange(channel_)
            channel_.basic_publish(exchange=self.computer, body=message, routing_key='',
                                   properties=pika.BasicProperties(delivery_mode=1))
            conn_.close()
        except Exception as e:
            print(e)

    def conn_close(self):
        try:
            self.conn.close()
        except Exception as e:
            print(e)




