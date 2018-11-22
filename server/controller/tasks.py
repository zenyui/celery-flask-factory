import datetime
import time
import logging
from celery import Celery

logger = logging.getLogger()
celery = Celery(__name__, autofinalize=False)

@celery.task(bind=True)
def wait_task(self, sleep_time):
    '''sample task that sleeps 5 seconds then returns the current datetime'''
    time.sleep(sleep_time)
    return datetime.datetime.now().isoformat()
