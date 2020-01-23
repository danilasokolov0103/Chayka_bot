import datetime
import parser
import creating_db
from celery import Celery
import logging
from celery.app.log import TaskFormatter
from celery.utils.log import get_task_logger
import celery.signals

@celery.signals.beat_init.connect
def on_beat_init_disable_connection_pool(sender, **kwargs):
    sender.app.conf.BROKER_POOL_LIMIT = 0

app = Celery('periodic', broker='redis://redis:6379/0')

logger = logging.getLogger()
sh = logging.StreamHandler()
sh.setFormatter(TaskFormatter('%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s'))
logger.setLevel(logging.INFO)
logger.addHandler(sh)

@app.task
def celery_schedule():
    parser.get_all_rooms_schedule()
    logging.info("Done task")
    print(datetime.datetime.now())
    return parser.get_all_rooms_schedule


app.conf.beat_schedule = {
    "get_shedule_every_30minutes_task": {
        "task": "periodic.celery_schedule",
        "schedule": 60.0 
    }
}



    




