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
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, room, time, status, day, date):
        self.room = room
        self.time = time
        self.status = status
        self.day = day
        self.date = date
    def __repr__(self):
        return '<Schedule {} {} {} {} {}>'.format(self.room, self.time, self.status, self.day, self.date)

# Создание таблицы
schedule_db.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_to_db(room, time, status, day, date):
        day_time_status = Schedule(room= room, time = time, status = status, day = day, date = date)
        session.add(day_time_status)
        session.commit()


def delete_expired_data():
    list_instance = session.query(Schedule) #создаем список из объектов дб
    max_time = list_instance[0].time_created #находим ближайшее время
    for item in (list_instance):
        if item.time_created > max_time:
            max_time = item.time_created

    for instance1 in list_instance: #удаляем из базы все, что не max_time
            if  instance1.time_created != max_time:
                session.delete(instance1)
                session.commit()