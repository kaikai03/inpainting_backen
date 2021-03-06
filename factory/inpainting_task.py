# coding: utf-8

import sys
sys.path.append('factory')

from celery import Celery
import yaml
from celery_once import QueueOnce
# 因为pycharm会把app设为根，所以此处会报找不到方法，但是不影响。
from monitor import Monitor
import threading
import time


__heart_beat_interval__ = 10

C_FAKEFORK=1

isWorker = False
heart_beat_timer = None

n_param = [sys.argv[i+1] for i,arg in enumerate(sys.argv) if arg=='-n']


if len(n_param) !=0:
    isWorker = True

if isWorker:
    __config_file__ = 'config.yaml'
    work_name = n_param[0].split("@")[0]
    print("name:",work_name)
else:
    __config_file__ = './factory/config.yaml'

with open(__config_file__, 'r') as f:
    content = yaml.load(f)
    broker = content['cel']['broker']
    backend = content['cel']['backend']
    backend_once = content['cel_once']['backend']

assert broker is not None
assert backend is not None

print(backend, broker)
app = Celery('inpainting_task', backend=backend, broker=broker)
app.conf.update(
    BROKER_HEARTBEAT=24*60*60*2,
    BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 3600}
)
app.conf.ONCE = {
  'backend': 'celery_once.backends.Redis',
  'settings': {
    'url': backend_once,
    'default_timeout': 60 * 60 * 12
  }
}

print('celery start up')

if isWorker:
    m = Monitor(work_name)
    m.publish_report_start()
    from task1 import add



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
    # 有个前提：work必须比app上线得晚,否则有潜在问题
    ret = app_celery.control.inspect().ping()
    print('ret:',ret,type(ret))
    if ret is None:
        return []
    return list(ret.keys())

# app.control.inspect().ping()
# app.control.inspect().stats()

##
def heart_beat_start(call_back = None):
    # print('celery worker heart beat',type(call_back))
    global heart_beat_timer
    heart_beat_timer = threading.Timer(__heart_beat_interval__,heart_beat_start,[call_back])
    heart_beat_timer.start()

    if hasattr(call_back, '__call__'):
        call_back(get_online_worker(app))
    else:
        print("celery:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), get_online_worker(app))

def heart_beat_stop():
    global heart_beat_timer
    if heart_beat_timer is None:
        return

    while heart_beat_timer.is_alive():
        heart_beat_timer.cancel()
        heart_beat_timer.cancel()
    heart_beat_timer = None


if isWorker:
    heart_beat_start()