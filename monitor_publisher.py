# coding: utf-8

from monitor_tmp import Monitor
import threading

import pika
import json


class Publisher:
    def __init__(self):
        self.credentials = pika.PlainCredentials('root', 'root')
        self.conn_param = pika.ConnectionParameters(
            host='106.14.20.200', port=5672, credentials=self.credentials, heartbeat=300)

    def connect(self):
        self.conn = pika.BlockingConnection(self.conn_param)
        self.channel = self.conn.channel()
        self.channel.exchange_declare(exchange=r'DESKTOP-QQDIIUS\\faker',
                                      durable=False, exchange_type='fanout')

    def publish(self, message):
        try:
            self.channel.basic_publish(exchange=r'DESKTOP-QQDIIUS\\faker',
                                       routing_key='', body=message,
                                       properties=pika.BasicProperties(delivery_mode=1))
        except Exception as e:
            self.connect()
            self.channel.basic_publish(exchange=r'DESKTOP-QQDIIUS\\faker',
                                       routing_key='', body=message,
                                       properties=pika.BasicProperties(delivery_mode=1))

    def conn_close(self):
        try:
            self.conn.close()
        except Exception as e:
            print(e)




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