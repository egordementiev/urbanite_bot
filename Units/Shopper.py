from Units.DataBaseConfig import Base
from sqlalchemy import Column, Integer, ARRAY, Boolean, Text
from typing import Union


class Shopper(Base):
    __tablename__ = 'shoppers'

    ID = Column(Integer, primary_key=True)
    title = Column(Text)
    description = Column(Text)
    material = Column(Text)
    price = Column(Text)
    photos = Column(ARRAY(Text))

    def __init__(self, ID: Union[str, int] = None, title: str = None,
                 description: str = None, material: str = None , price: int = None, photos: list = None):
        self.ID = ID
        self.title = title
        self.description = description
        self.material = material
        self.price = price
        self.photos = photos

    def render_mini_profile(self):
        return f'({self.ID}) {self.title}, цена: {self.price}грн'

    def render_big_profile(self):
        return f'Название: {self.title}\n' \
               f'\n' \
               f'Описание: {self.description}\n' \
               f'\n' \
               f'Материал: {self.material}\n' \
               f'\n' \
               f'Размер: (35х41 см) 135 г/кв.м\n' \
               f'\n' \
               f'Цена: {self.price}грн'

    def __repr__(self):
        return f'({self.ID}) {self.title}, цена: {self.price}грн | фотографии = {self.photos}'


class Statistic(Base):
    _tablename_ = "statistics"

    ID = Column(Integer)
    stat_name = Column(Text)
    stat = Column(Text)

    def __init__(self, ID, stat_name, stat):
        self.ID = ID
        self.stat_name = stat_name
        self.stat = stat

    def __repr__(self):
        return f'({self.ID}) {self.stats_name} = {self.stat}'
