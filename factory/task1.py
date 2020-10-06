# coding: utf-8

import sys
sys.path.append('factory')
import time
from celery_once import QueueOnce

from inpainting_task import app
# import inpainting_task

@app.task(base=QueueOnce)
def add(x, y):
    time.sleep(10)
    return x + y