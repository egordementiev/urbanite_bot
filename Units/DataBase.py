from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Units.DataBaseConfig import Base
from abc import ABC, abstractmethod
from Units.Shopper import Shopper, Statistic
from Units.User import User


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
    def __init__(self, port='5432', host='localhost', password='fagSxElh3f2c5_', dbname='postgres', user='postgres'):
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
        old_user.cart = user.cart
        old_user.is_admin = user.is_admin
        print(session.dirty)
        session.commit()

    def get_user(self, ID: int) -> User:
        session = Session(self.engine)
        user = session.query(User).filter(ID == ID).first()
        session.close()
        return user

    def add_shopper(self, shopper: Shopper):
        session = Session(self.engine)
        # try:
        print(shopper)
        session.add(shopper)
        session.commit()
        # except Exception as e:
        #     print(e)
        #     return False
        # finally:
        #     session.close()

    def update_shopper(self, shopper: Shopper):
        session = Session(self.engine)
        old_user = session.query(User).filter_by(ID=shopper.ID).first()
        session.delete(old_user)
        session.add(shopper)
        print(session.dirty)
        session.commit()
        session.close()

    def del_shopper(self, shopper: Shopper):
        session = Session(self.engine)
        session.delete(shopper)
        session.commit()
        session.close()

    def get_shopper(self, ID: int) -> Shopper:
        session = Session(self.engine)
        shopper = session.query(Shopper).filter(ID == ID).first()
        session.close()
        return shopper

    def get_shoppers(self) -> Shopper:
        session = Session(self.engine)
        shoppers = session.query(Shopper).all()
        session.close()
        return shoppers
