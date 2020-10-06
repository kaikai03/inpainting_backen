# coding: utf-8
# from __future__ import absolute_import # 使用绝对导入

import sys
sys.path.append('factory')
import time
from celery_once import QueueOnce

from inpainting_task import app


@app.task(base=QueueOnce)
def add(x, y):
    time.sleep(10)
    return x + y