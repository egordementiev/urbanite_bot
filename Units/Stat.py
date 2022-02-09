from Units.DataBaseConfig import Base
from sqlalchemy import Column, Integer, ARRAY, Boolean, Text
from typing import Union


class Stat(Base):
    __tablename__ = 'stats'

    ID = Column(Integer, primary_key=True)
    title = Column(Text, unique=True)
    users = Column(Integer)

    def __init__(self, ID, title, users):
        self.ID = ID
        self.title = title
        self.users = users

    def __repr__(self):
        return f'({self.ID}) переходы с {self.title} = {self.users}'