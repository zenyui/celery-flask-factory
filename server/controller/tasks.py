import datetime
import time
import random
import math
import json
import logging
from google.cloud import storage
from celery import Celery, Task
from flask import has_app_context

logger = logging.getLogger()
celery = Celery(__name__, autofinalize=False)

@celery.task(bind=True)
def add(self, x, y):
    return x+y

@celery.task(bind=True)
def sample_task(self):
    '''sample task that sleeps 5 seconds then returns the current datetime'''
    time.sleep(5)
    return datetime.datetime.now().isoformat()
