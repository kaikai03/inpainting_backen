from celery import Celery
import yaml
from celery_once import QueueOnce

__config_file__ = 'config.yaml'

with open(__config_file__, 'r') as f:
    content = yaml.load(f)
    broker = content['cel']['broker']
    backend = content['cel']['backend']
    backend_once = content['cel_once']['backend']

assert broker is not None
assert backend is not None

print(backend, broker)
app = Celery('inpainting_task', backend=backend, broker=broker)
app.conf.ONCE = {
  'backend': 'celery_once.backends.Redis',
  'settings': {
    'url': backend_once,
    'default_timeout': 60 * 60 * 2
  }
}

import time

@app.task(base=QueueOnce)
def add(x, y):
    time.sleep(10)
    return x + y



if False:
    # celery -A inpainting_task worker --loglevel=info -P eventlet -Q computerName
    # celery -A inpainting_task worker --loglevel=info -P eventlet -c 1 -n worker1@%h
    # celery -A inpainting_task worker --loglevel=info -P eventlet -c 1 -n worker2@%h
    # celery multi stopwait w1 -A inpainting_task -l info
    # celery -A inpainting_task status
    # celery -A inpainting_task inspect active
    # from inpainting_task import add

    s = add.signature((2, 2), countdown=1)
    result = s.delay()

    result = add.delay(4, 8)
    result = add.delay(4, 9)
    result = add.delay(4, 10)
    result = add.delay(4, 11)
    result = add.delay(4, 12)
    result = add.delay(4, 13)
    # result = add.apply_async(args=[12, 13], queue='computerName', routing_key='computerName')
    result = add.apply_async(args=[12, 13])
    result.ready()
    result.successful()
    result.failed()
    result.state  ## PENDING -> STARTED -> SUCCESS
    result.get(timeout=1)
    result.get()
    result.get(propagate=False)
    result.traceback
    result.forget()
    result.backend

    # TODO: worker name 用compute name，每次页面上线时，请求一下，就知道哪些节点在线了。



def get_online_worker(app_celery):
    ## 这样可以拿到在线列表
    # 不过这里效率有问题，需要异步
    # 有个前提：work必须比app上线得晚
    return list(app_celery.control.inspect().active_queues().keys())
print(get_online_worker(app))


import json
import base64

def get_base64_from_file(filepath):
    with open(filepath, "rb") as f:
        bytes_content = f.read() # bytes
        bytes_64 = base64.b64encode(bytes_content)
    return bytes_64.decode('utf-8') # bytes--->str  (remove `b`)

def get_base85_from_file(filepath):
    with open(filepath, "rb") as f:
        bytes_content = f.read() # bytes
        bytes_85 = base64.b85encode(bytes_content)
    return bytes_85.decode('utf-8') # bytes--->str  (remove `b`)

