# coding: utf-8

import sys
sys.path.append('factory')
sys.path.append('./factory/')

from celery import Celery
import yaml
from celery_once import QueueOnce
# 因为pycharm会把app设为根，所以此处会报找不到方法，但是不影响。
from monitor import Monitor
import threading

__config_file__ = 'config.yaml'
__heart_beat_interval__ = 10

n_param = [sys.argv[i+1] for i,arg in enumerate(sys.argv) if arg=='-n']

assert len(n_param) == 1
work_name = n_param[0].split("@")[0]
print("name:",work_name)
heart_beat_timer = None

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

print('celery start up')




import time

@app.task(base=QueueOnce)
def add(x, y):
    time.sleep(10)
    return x + y

m = Monitor(work_name)
m.publish_report_start()


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
    return list(app.control.inspect().ping().keys())
#print(get_online_worker(app))
# app.control.inspect().active_queues()
# app.control.inspect().stats()
# app.control.inspect().clock()
# app.control.inspect().ping()
# app.worker_main()

def heart_beat_start():
    global heart_beat_timer
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),app.control.inspect().ping())
    heart_beat_timer = threading.Timer(__heart_beat_interval__,heart_beat_start)
    heart_beat_timer.start()



def heart_beat_stop():
    global heart_beat_timer
    if heart_beat_timer is None:
        return

    while heart_beat_timer.is_alive():
        heart_beat_timer.cancel()
        heart_beat_timer.cancel()
    heart_beat_timer = None