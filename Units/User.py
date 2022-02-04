from Units.DataBaseConfig import Base
from sqlalchemy import Column, Integer, ARRAY, Boolean


class User(Base):
    __tablename__ = 'users'

    ID = Column(Integer, primary_key=True)
    cart = Column(ARRAY(Integer))
    is_admin = Column(Boolean)

    def __init__(self, ID, cart, is_admin):
        self.ID = ID
        self.cart = cart
        self.is_admin = is_admin

    def get_id(self):
        return self.ID

    def get_cart(self):
        return self.cart

    def get_is_admin(self):
        return self.is_admin

    def set_cart(self, cart):
        self.cart = cart

    def __repr__(self):
        return f'({self.ID}) cart = {self.cart}, is_admin = {self.is_admin}'
