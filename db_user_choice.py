from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased
from sqlalchemy import DateTime
from sqlalchemy import func


engine = create_engine('sqlite:///user_choice_db.db', echo=False)

user_choice_db = declarative_base()

class User_choice(user_choice_db):
    __tablename__='выбор юзера'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    chat_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    chosen_room =Column (String, nullable=True)
    chosen_day = Column(String, nullable = True)
    chosen_week = Column(String, nullable = True)

def __init__(self, chat_id, user_id, chosen_room, chosen_day, chosen_week):
    self.chat_id = chat_id
    self.user_id = user_id
    self.chosen_room = chosen_room
    self.chosen_day = chosen_day
    self.chosen_week = chosen_week
def __repr__(self):
    return'<User choice {} {} {} {} {}>'.format(self.chat_id, self.user_id, self.chosen_room, self.chosen_day, self.chosen_week)

user_choice_db.metadata.create_all(engine)

Session = sessionmaker(bind= engine)
session = Session()


