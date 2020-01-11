from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased
from sqlalchemy import DateTime
from sqlalchemy import func



engine = create_engine('sqlite:///schedule_db.db', echo=False)

schedule_db = declarative_base()
class Schedule(schedule_db):
    __tablename__ = 'расписание_комнат'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    room = Column(String, nullable=True)
    time = Column(String, nullable=True)
    status = Column(String, nullable=True)
    day = Column(String, nullable=True)
    date = Column(String,nullable=True)
    parsing_time = Column(String, nullable = True)
    parsing_time_int = Column(Integer, nullable=True)

    
    def __init__(self, room, time, status, day, date, parsing_time, parsing_time_int):
        self.room = room
        self.time = time
        self.status = status
        self.day = day
        self.date = date
        self.parsing_time = parsing_time
        self.parsing_time_int = parsing_time_int
    def __repr__(self):
        return '<Schedule {} {} {} {} {} {} {}>'.format(self.room, self.time, self.status, self.day, self.date, self.parsing_time, self.parsing_time_int)

# Создание таблицы
schedule_db.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_to_db(room, time, status, day, date, parsing_time, parsing_time_int):
        day_time_status = Schedule(room= room, time = time, status = status, day = day, date = date, parsing_time = parsing_time, parsing_time_int = parsing_time_int)
        session.add(day_time_status)
        session.commit()

db_elements = session.query(Schedule) #создаем список из объектов дб

def max_time():#находим ближайшее время
    max_time = db_elements[0].parsing_time_int
    for item in (db_elements):
        if item.parsing_time_int > max_time:
            max_time = item.parsing_time_int
    return max_time

def delete_expired_data():#удаляем из базы все, что не max_time
    time = max_time()
    for instance1 in db_elements: 
            if  instance1.parsing_time_int != time:
                session.delete(instance1)
                session.commit()

def get_info(user_time):
    data = []
    for room in session.query(Schedule).filter(Schedule.time == user_time).filter(Schedule.status=='free'):
            data.append([room.room, room.date, room.day])
    return(data)
