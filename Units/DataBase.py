from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from Units.Shopper import Shopper
from Units.User import User
from Units.SiteUser import SiteUser
from Units.Stat import Stat
from typing import Union
from Units.DataBaseConfig import Base


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

    @abstractmethod
    def get_site_user(self, ID: int):
        pass


class SQLAlchemy(DataBase):
    def __init__(self, port='5434', host='localhost', password='123', dbname='postgres', user='postgres'):
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
        print(session.query(User).filter(User.ID == user.ID).all())
        old_user = session.query(User).filter_by(ID=user.ID).first()
        print(old_user)
        old_user.cart = user.cart
        old_user.is_admin = user.is_admin
        print(session.dirty)
        session.commit()

    def get_user(self, ID: int) -> Union[User, None]:
        session = Session(self.engine)
        try:
            print(session.query(User).filter_by(ID=ID).all())
            user = session.query(User).filter_by(ID=ID).first()
            print(user)
        except Exception as e:
            print(e)
            return None
        session.close()
        return user

    def get_users(self):
        session = Session(self.engine)
        users = session.query(User).all()
        session.close()
        return users

    def add_site_user(self, site_user: SiteUser):
        session = Session(self.engine)
        try:
            session.add(site_user)
            session.commit()
        except:
            return False
        finally:
            session.close()

    def update_site_user(self, site_user: SiteUser):
        session = Session(self.engine)
        print(session.query(User).filter(User.ID == site_user.ID).all())
        old_site_user = session.query(User).filter_by(ID=site_user.ID).first()
        print(old_site_user)
        old_site_user.email = site_user.email
        print(session.dirty)
        session.commit()

    def get_site_user(self, ID: int) -> Union[SiteUser, None]:
        session = Session(self.engine)
        try:
            print(session.query(SiteUser).filter_by(ID=ID).all())
            user = session.query(SiteUser).filter_by(ID=ID).first()
            print(user)
        except Exception as e:
            print(e)
            session.close()
            return None
        session.close()
        return user

    def get_site_user_by_email(self, email: str) -> Union[SiteUser, None]:
        session = Session(self.engine)
        try:
            print(session.query(SiteUser).filter_by(email=email).all())
            user = session.query(SiteUser).filter_by(email=email).first()
            print(user)
        except Exception as e:
            print(e)
            session.close()
            return None
        session.close()
        return user

    def get_site_users(self) -> list:
        session = Session(self.engine)
        users = session.query(SiteUser).all()
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
            print(session.query(Shopper).filter_by(ID=ID).all())
            shopper = session.query(Shopper).filter_by(ID=ID).first()
            print(shopper)
        except:
            return None
        session.close()
        return shopper

    def get_shoppers(self) -> list:
        session = Session(self.engine)
        shoppers = session.query(Shopper).all()
        session.close()
        return shoppers

    def add_stat(self, stat):
        session = Session(self.engine)
        try:
            print(stat)
            session.add(stat)
            session.commit()
        except Exception as e:
            print(e)
            return False
        finally:
            session.close()

    def update_stat(self, stat: Stat):
        session = Session(self.engine)
        old_stat = session.query(Stat).filter_by(ID=stat.ID).first()
        print(f'old_stat = {old_stat}')
        print(f'new_stat = {stat}')
        old_stat.title = stat.title
        old_stat.users = stat.users
        session.commit()
        session.close()

    def get_stat_by_title(self, title):
        session = Session(self.engine)
        print(session.query(Stat).filter_by(title=title).all())
        shopper = session.query(Stat).filter_by(title=title).first()
        print(shopper)
        session.close()
        return shopper

    def get_stats(self):
        session = Session(self.engine)
        stats = session.query(Stat).all()
        session.close()
        return stats
