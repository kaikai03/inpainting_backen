from celery import Celery
import yaml

__config_file__ = 'config.yaml'

with open(__config_file__, 'r') as f:
    content = yaml.load(f)
    broker = content['cel']['broker']
    backend = content['cel']['backend']

assert broker is not None
assert backend is not None

print(backend, broker)
app = Celery('tasks', backend=backend, broker=broker)

@app.task
def add(x, y):
    return x + y


if False:
    # celery -A inpainting_task worker --loglevel=info -P eventlet
    # from inpainting_task import add

    result = add.delay(4, 10)
    result.ready()
    result.get(timeout=1)
    result.get()
    result.get(propagate=False)
    result.traceback