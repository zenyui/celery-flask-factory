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
def test(self):
    return datetime.datetime.now().isoformat()

@celery.task(bind=True)
def test_flask_context(self):
    return {'has_app_context': has_app_context()}

@celery.task(bind=True)
def make_json(self):
    time.sleep(5)

    # get bucket
    bucket_name = 'funnel-cache'
    bucket = storage.Client().get_bucket(bucket_name)

    # get data
    cols, data = generate_query()

    pagesize = 1000
    pages = math.ceil(len(data) / pagesize)

    for page in range(pages):
        time.sleep(5)

        loaded_page = page + 1

        # write page i to bucket
        blob_name = '{task_id}--{loaded_page}'.format(task_id=self.request.id, loaded_page=loaded_page)
        blob = storage.Blob(blob_name, bucket)
        str_data = json.dumps(data[page*pagesize:(page+1)*pagesize])
        blob.upload_from_string(str_data)

        # update task status
        self.update_state(state='CACHING', meta={'loaded_page': loaded_page, 'maxpage': pages})

    return {'loaded_page': loaded_page , 'maxpage': pages}

def generate_query():
    cols = ['A','B','C','D']
    data = [[random.randint(0,100) for _ in range(4)] for j in range(10000)]
    return cols, data

def get_task_result(task_id, page_id):
    pass
