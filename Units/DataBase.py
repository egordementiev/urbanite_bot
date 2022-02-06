from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Units.DataBaseConfig import Base
from abc import ABC, abstractmethod
from Units.Shopper import Shopper
from Units.User import User
from typing import Union


class DataBase(ABC):
    @abstractmethod
    def add_user(self, user: User):
        pass

    @abstractmethod
    def update_user(self, user: User):
        pass

    @abstractmethod
    def add_shopper(self, shopper: Shopper):
        pass

    @abstractmethod
    def update_shopper(self, shopper: Shopper):
        pass

    @abstractmethod
    def del_shopper(self, shopper: Shopper):
        pass


class SQLAlchemy(DataBase):
    def __init__(self, port='5432', host='localhost', password='123', dbname='postgres', user='postgres'):
        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
        Base.metadata.create_all(self.engine)

    def add_user(self, user: User):
        session = Session(self.engine)
        try:
            session.add(user)
            session.commit()
        except:
            return False
        finally:
            session.close()

    def update_user(self, user: User):
        session = Session(self.engine)
        old_user = session.query(User).filter_by(ID=user.ID).first()
        print(old_user)
        old_user.cart = user.cart
        old_user.is_admin = user.is_admin
        print(session.dirty)
        session.commit()

    def get_user(self, ID: int) -> Union[User, None]:
        session = Session(self.engine)
        try:
            user = [user for user in self.get_users() if user.ID == ID][0]
        except IndexError:
            return None
        session.close()
        return user

    def get_users(self):
        session = Session(self.engine)
        users = session.query(User).all()
        session.close()
        return users

    def add_shopper(self, shopper: Shopper):
        session = Session(self.engine)
        try:
            print(shopper)
            session.add(shopper)
            session.commit()
        except Exception as e:
            print(e)
            return False
        finally:
            session.close()

    def update_shopper(self, shopper: Shopper):
        session = Session(self.engine)
        old_shopper = session.query(Shopper).filter_by(ID=shopper.ID).first()
        print(f'old user = {old_shopper}')
        old_shopper.title = shopper.title
        old_shopper.description = shopper.description
        old_shopper.material = shopper.material
        old_shopper.price = shopper.price
        old_shopper.photos = shopper.photos
        print(session.dirty)
        session.commit()
        session.close()

    def del_shopper(self, shopper: Shopper):
        session = Session(self.engine)
        session.delete(shopper)
        session.commit()
        session.close()

    def get_shopper(self, ID: int) -> Union[Shopper, None]:
        session = Session(self.engine)
        try:
            shopper = [shopper for shopper in session.query(Shopper).all() if shopper == ID][0]
        except IndexError:
            return None
        session.close()
        return shopper

    def get_shoppers(self) -> Shopper:
        session = Session(self.engine)
        shoppers = session.query(Shopper).all()
        session.close()
        return shoppers
