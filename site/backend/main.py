import os
import flask
from flask import Flask, render_template, request, flash, redirect, url_for
from Units.DataBase import SQLAlchemy, DataBase
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash
from validate_email import validate_email


class UserLogin:
    """ Класс для описания пользователя, который вошел в аккаунт """
    def fromDB(self, site_user_id, db: DataBase):
        self.__user = db.get_site_user(site_user_id)
        return self

    def create(self, reader):
        self.__user = reader
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.ID)


database = SQLAlchemy()

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

login_manager = LoginManager(app)  # Создаем менеджер для регистрации и входа в аккаунт пользователями
login_manager.login_view = 'api_login'

app.config['DEBUG'] = True  # Ставим DEBUG = True для тестов, потом нужно поменять на False
app.config['SECRET_KEY'] = 'SsdSvdhstebfFSvfhsvdCFDDGCEVsbfgsvfcaFCbsdfscFSV'  # Выгружаем из окружения секретный ключ


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, database)  # Берем пользователя из базы данных


@app.route('/')
def index():
    """ Главная страница сайта """
    user = database.get_site_user(current_user.get_id())  # Берем пользователя из библиотеки
    shoppers = database.get_shoppers()
    return render_template('index.html', active="home",
                           popular_shopper=shoppers[randint(0, len(shoppers)-1)])


@app.route('/catalog')
def catalog():
    """ Главная страница сайта """
    user = database.get_site_user(current_user.get_id())  # Берем пользователя из библиотеки
    shoppers = database.get_shoppers()
    return render_template('catalog.html', active="catalog",
                           popular_shopper=shoppers[randint(0, len(shoppers)-1)])


app.run()
