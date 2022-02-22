from Units.DataBaseConfig import Base
from sqlalchemy import Column, Integer, ARRAY, Boolean, Text


class SiteUser(Base):
    __tablename__ = 'site_users'

    ID = Column(Integer, primary_key=True)
    cart = Column(ARRAY(Integer))
    is_admin = Column(Boolean)

    email = Column(Text)
    password = Column(Text)

    def __init__(self, ID, cart, is_admin, email, password):
        self.ID = ID
        self.user = cart
        self.is_admin = is_admin
        self.email = email
        self.password = password

    def __repr__(self):
        return f'({self.ID}) cart = {self.cart}, is_admin = {self.is_admin}'
