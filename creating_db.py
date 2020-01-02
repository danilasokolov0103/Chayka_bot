from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased
from sqlalchemy import DATETIME




engine = create_engine('sqlite:///schedule_db.db', echo=False)

schedule_db = declarative_base()
class Schedule(schedule_db):
    __tablename__ = 'расписание_комнат'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    room = Column(String, nullable=True)
    time = Column(String, nullable=True)
    status = Column(String, nullable=True)
    day = Column(String, nullable=True)
    parsing_time = Column(DATETIME, nullable=True)
    
    def __init__(self, room, time, status, day, parsing_time):
        self.room = room
        self.time = time
        self.status = status
        self.day = day
        self.parsing_time = parsing_time
    def __repr__(self):
        return '<Schedule {} {} {} {} {}>'.format(self.room, self.time, self.status, self.day, self.parsing_time)

# Создание таблицы
schedule_db.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_to_db(room, time, status, day, parsing_time):
        day_time_status = Schedule(room= room, time = time, status = status, day = day, parsing_time = parsing_time)
        session.add(day_time_status)
        session.commit()

# for instance in session.query(Schedule).order_by(Schedule.id): 
#     print (instance.room, instance.status)
# def get_info(prefered_time):
#     result = []
#     for room in session.query(Schedule).filter(Schedule.status=='free').filter(Schedule.time == prefered_time):
#         result.append(room)
#     return result


# def get_info():
#     for room in session.query(Schedule).filter(Schedule.status=='free').filter(Schedule.time=='9–10'):
#         print(room)

# result1 = []
# result1.append(get_info(result, '9–10'))
# print(result1)
# get_info()