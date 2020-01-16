import datetime
import parser
import creating_db
from celery import Celery

app = Celery('periodic', broker='redis://localhost:6379/0')


@app.task
def celery_schedule():
    parser.get_all_rooms_schedule()
    print(datetime.datetime.now())
    return parser.get_all_rooms_schedule


app.conf.beat_schedule = {
    "get_shedule_every_30minutes_task": {
        "task": "periodic.celery_schedule",
        "schedule": 1800.0 
    }
}



    




